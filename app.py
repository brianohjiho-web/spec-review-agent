"""SpecCheck AI web app. Run it with: streamlit run app.py"""
import json
import os
import re
from html import escape
from pathlib import Path

import streamlit as st
from anthropic import Anthropic, APIError
from dotenv import load_dotenv

from speccheck.agent import AgentError, SpecAgent
from speccheck.catalog import load_catalog
from speccheck.checks import RULES
from speccheck.metals import CHARTS, ENTERED, LB_PER_METRIC_TON, LIVE, latest_prices, material_cost, per_lb
from speccheck.models import CheckResult, ProductCheck, Review, SpecRequirements
from speccheck.pdf import SpecFileError, read_pdf
from speccheck.review import build_review, to_csv
from speccheck.settings import DailyCounter, app_password, daily_limit, has_api_key, password_ok
from speccheck.theme import CSS, FOOTER, HEADER

ROOT = Path(__file__).parent
SAMPLES = ROOT / "data" / "samples"
EQUIPMENT = {
    "Utility": (":material/electric_bolt:", {"Utility service": "mill_creek_utility"}),
    "Transformer": (":material/settings_input_component:", {"Transformer": "summit_transformer"}),
    "Bus": (":material/view_stream:", {
        "Cable bus": "ridgeline_cable_bus",
        "Iso phase bus": "lakeshore_iso_bus",
        "Non-seg bus": "prairie_non_seg",
    }),
    "Switchgear": (":material/dashboard:", {
        "Medium-voltage switchgear": "red_oak_mv",
        "Low-voltage switchgear": "harbor_lv",
        "Outdoor switchgear, 34.5 kV": "high_desert_mv",
    }),
    "UPS": (":material/battery_charging_full:", {"UPS": "orion_ups"}),
    "Server racks": (":material/dns:", {"Server racks": "atlas_server_racks"}),
}
STATUS_LABELS = {"PASS": "Pass", "FAIL": "Fail", "REVIEW": "Review"}
SHORT_NAMES = {
    "Rated maximum voltage": "Max voltage",
    "Impulse withstand (BIL)": "BIL",
    "Continuous current": "Current",
    "Short-circuit rating": "Short circuit",
    "Ambient temperature": "Ambient temp",
    "Site altitude": "Altitude",
    "Price": "Budget",
}

load_dotenv(ROOT / ".env")
st.set_page_config(page_title="SpecCheck AI", layout="wide")


def load_streamlit_secrets() -> None:
    """Copies Streamlit Cloud secrets into settings, if any exist."""
    try:
        secrets = dict(st.secrets)
    except Exception:  # No secrets file, which is normal on a computer.
        return
    for name in ("ANTHROPIC_API_KEY", "APP_PASSWORD", "DAILY_REVIEW_LIMIT", "SPECCHECK_MODEL"):
        if name in secrets and not os.getenv(name):
            os.environ[name] = str(secrets[name])


load_streamlit_secrets()


@st.cache_data
def catalog() -> list[dict]:
    return load_catalog()


@st.cache_resource
def review_counter() -> DailyCounter:
    return DailyCounter()


@st.cache_data
def saved_spec(sample: str) -> tuple[dict, str]:
    text = read_pdf((SAMPLES / f"{sample}.pdf").read_bytes())
    data = json.loads((SAMPLES / f"{sample}.requirements.json").read_text(encoding="utf-8"))
    return data, text


def saved_review(sample: str) -> tuple[Review, str]:
    data, text = saved_spec(sample)
    return build_review(SpecRequirements(**data), catalog(), text), text


def html(content: str) -> None:
    st.markdown(content, unsafe_allow_html=True)


def label(text: str) -> None:
    html(f'<span class="sc-label">{escape(text)}</span>')


def usd(text: str) -> str:
    return re.sub(r"(\d+(?:\.\d+)?) USD", lambda m: f"${float(m.group(1)):,.0f}", text)


def required_text(result: CheckResult) -> str:
    text = re.sub(r"^at least (.*)$", r"\1 min", result.required)
    return usd(re.sub(r"^at most (.*)$", r"\1 max", text))


def item_name(result: CheckResult) -> str:
    rule = RULES.get(result.requirement.parameter)
    return SHORT_NAMES.get(rule.label, rule.label) if rule else "Other"


def note_text(result: CheckResult) -> str:
    return result.note.replace(
        "This item is outside the automatic checks. An engineer must review it.",
        "Needs engineer review.",
    )


def compliance_table(check: ProductCheck, status: str) -> str:
    results = [r for r in check.results if status == "All" or STATUS_LABELS[r.status] == status]
    rows = []
    for r in results:
        product = "—" if r.product_value == "Not checked" else usd(r.product_value)
        priority = "Must have" if r.requirement.mandatory else "Preferred"
        note = f'<div class="sc-note">{escape(note_text(r))}</div>' if r.note else ""
        section = f'<div class="sc-tag">Section {escape(r.requirement.section)}</div>' if r.requirement.section else ""
        rows.append(
            f'<tr class="sc-row-{r.status}"><td><span class="sc-chip {r.status}">{STATUS_LABELS[r.status]}</span></td>'
            f'<td><div class="sc-name">{escape(item_name(r))}</div><div class="sc-tag">{priority}</div></td>'
            f'<td>{escape(required_text(r))}</td><td>{escape(product)}{note}</td>'
            f'<td><div class="sc-quote">“{escape(r.requirement.source_quote)}”</div>{section}</td></tr>'
        )
    body = "".join(rows) or '<tr><td colspan="5">No items with this status.</td></tr>'
    return (
        '<div class="sc-scroll"><table><thead><tr><th>Status</th><th>Requirement</th>'
        f"<th>Spec needs</th><th>Product has</th><th>From the spec</th></tr></thead><tbody>{body}</tbody></table></div>"
    )


def money(value) -> str:
    return "—" if value is None else f"${value:,.0f}"


@st.cache_data(ttl=12 * 60 * 60, show_spinner=False)
def metal_prices() -> dict:
    return latest_prices()


CALCULATOR = {**{k: (v, "lb") for k, v in LIVE.items()}, **ENTERED}


def entered_prices() -> dict:
    return {key: st.session_state.get(f"price-{key}") or 0.0 for key in CALCULATOR}


def materials_table(product_id: str) -> str:
    product = next((p for p in catalog() if p["id"] == product_id), None)
    if not product or not product.get("materials_lb"):
        return ""
    rows = material_cost(product["materials_lb"], metal_prices(), entered_prices())
    if not rows:
        return ""
    total = sum(r["cost"] for r in rows if r["cost"])
    share = price_split(product["price_usd"], rows, total) if product.get("price_usd") else ""
    return (
        '<div class="sc-type" style="margin-top:10px;background:#e4f1f2;border-color:#dfe5ea">'
        f'<div class="sc-type-kicker">Material cost estimate: {escape(product["name"])}</div>'
        f'<div style="font-size:2rem;font-weight:600;line-height:1.15">{money(total)}</div></div>{share}'
    )


def price_split(price: float, rows: list, total: float) -> str:
    """Splits the product price into each material plus other costs, adding up to 100%."""
    def pct(value):
        share = value / price * 100
        return f"{share:.1f}%" if share < 1 else f"{share:.0f}%"

    parts = [(r["name"], r["cost"], False) for r in rows if r["cost"]]
    parts.append(("Other costs (labor, parts, overhead)", max(0, price - total), True))
    body = "".join(
        f'<div class="sc-split-row"><span>{escape(name)}</span>'
        f'<div class="sc-split-bar"><span style="width:{max(0.5, value / price * 100):.2f}%;background:{"#566575" if other else "#0b6e76"}"></span></div>'
        f'<span class="sc-split-num">{money(value)}</span><span class="sc-split-num" style="color:#566575">{pct(value)}</span></div>'
        for name, value, other in parts
    )
    return f'<div class="sc-split"><b>Product price: {money(price)} = 100%</b>{body}</div>'


def price_inputs() -> None:
    prices = metal_prices()
    with st.expander("Material price calculator"):
        st.caption("Copper, aluminum, lead, and nickel use FRED prices unless you type your own. "
                   "Steel, electrical steel, lithium, and transformer oil need a price you enter. Leave a box blank to skip it.")
        keys = list(CALCULATOR)
        for row in (keys[:4], keys[4:]):
            for column, key in zip(st.columns(4), row):
                name, unit = CALCULATOR[key]
                hint = f"{per_lb(prices[key]):.2f} from FRED" if key in LIVE else "Enter a price"
                column.number_input(f"{name} ($/{unit})", min_value=0.0, step=0.05, format="%.2f",
                                    value=None, placeholder=hint, key=f"price-{key}")


def sparkline(history: list, label: str, unit: str, index: bool = False) -> str:
    """A small line chart drawn as SVG. Hovering a point shows its month and price."""
    width, height, left, right, top, bottom = 260, 96, 4, 8, 10, 18
    values = [v for _, v in history]
    low, high = min(values), max(values)
    pad = (high - low) * 0.12 or 1

    def x(i):
        return left + (width - left - right) * i / (len(history) - 1)

    def y(v):
        return top + (height - top - bottom) * (1 - (v - (low - pad)) / ((high + pad) - (low - pad)))

    points = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(values))
    base = height - bottom
    dots = "".join(
        f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="7" fill="transparent"><title>{month(d)}: {f"{v:,.1f}" if index else f"${v:,.2f}{unit}"}</title></circle>'
        for i, (d, v) in enumerate(history)
    )
    return (
        f'<svg viewBox="0 0 {width} {height}" style="width:100%;height:auto;display:block" role="img" '
        f'aria-label="{escape(label)} price, last 12 months">'
        f'<line x1="{left}" x2="{width - right}" y1="{base}" y2="{base}" stroke="#dfe5ea"/>'
        f'<polygon points="{x(0):.1f},{base} {points} {x(len(values) - 1):.1f},{base}" fill="#0b6e76" opacity=".1"/>'
        f'<polyline points="{points}" fill="none" stroke="#0b6e76" stroke-width="2" stroke-linejoin="round"/>'
        f'<circle cx="{x(len(values) - 1):.1f}" cy="{y(values[-1]):.1f}" r="4" fill="#0b6e76" stroke="#fff" stroke-width="2"/>'
        f'<text x="{left}" y="{height - 4}" font-size="10" fill="#566575">{month(history[0][0])}</text>'
        f'<text x="{width - right}" y="{height - 4}" font-size="10" fill="#566575" text-anchor="end">{month(history[-1][0])}</text>'
        f"{dots}</svg>"
    )


def month(date: str) -> str:
    year, number = date[:4], int(date[5:7])
    names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return f"{names[number - 1]} {year[2:]}"


def price_charts() -> None:
    prices = metal_prices()
    cards = ""
    for key, (name, kind, note) in CHARTS.items():
        if kind == "none":
            cards += (f'<div class="sc-trend"><div class="sc-tag" style="font-weight:600">{name}</div>'
                      f'<p class="sc-small" style="margin:0">{note}. Enter your own price in the calculator.</p></div>')
            continue
        history = [[d, v / LB_PER_METRIC_TON if kind == "ton" else v] for d, v in prices[key]["history"]]
        first, last = history[0][1], history[-1][1]
        change = (last - first) / first * 100
        arrow, color = ("▲ +", "#17603a") if change >= 0 else ("▼ ", "#96231a")
        if kind == "index":
            shown, unit = f"Index {last:,.1f}", ""
        else:
            unit = "/bbl" if kind == "barrel" else "/lb"
            shown = f"${last:,.2f}{unit}"
        sub = f'<div class="sc-tag">{note}</div>' if note else ""
        cards += (
            f'<div class="sc-trend"><div class="sc-tag" style="font-weight:600">{name}</div>{sub}'
            f'<div><b style="font-size:1.15rem">{shown}</b> '
            f'<span style="font-size:.78rem;color:{color}">{arrow}{change:.0f}% in 12 mo</span></div>'
            f"{sparkline(history, name, unit, kind == 'index')}</div>"
        )
    html(
        '<div class="sc-h2" style="font-size:1.05rem;margin-top:22px">Price trends, last 12 months</div>'
        f'<div class="sc-trends">{cards}</div>'
    )


def products_table(review: Review) -> str:
    rows = "".join(
        f'<tr><td>{escape(c.product_name)}</td><td class="sc-num">{money(c.price_usd)}</td>'
        f'<td class="sc-num">{c.mandatory_fails}</td>'
        f'<td class="sc-num">{c.preferred_misses}</td><td class="sc-num">{c.reviews}</td></tr>'
        for c in review.ranked
    )
    return (
        '<div class="sc-scroll small"><table><thead><tr><th>Product</th><th>Price</th><th>Must-haves missed</th>'
        f"<th>Preferred items missed</th><th>To review</th></tr></thead><tbody>{rows}</tbody></table></div>"
    )


def result_panel(review: Review) -> str:
    best = review.ranked[0]
    match = bool(review.recommended_id)
    kicker = "Best match" if match else "No full match"
    title = best.product_name if match else "No product meets every must-have item"
    closest = "" if match else f'<p class="sc-small" style="margin-top:2px">Closest option: {escape(best.product_name)}</p>'
    chip = '<span class="sc-chip PASS">No must-haves failed</span>' if match else '<span class="sc-chip FAIL">Gaps found</span>'
    summary = f"<p>{escape(review.summary)}</p>" if review.summary else ""
    questions = "".join(f"<li>{escape(q)}</li>" for q in review.customer_questions)
    questions = f'<p class="sc-small">Questions for the customer:</p><ul>{questions}</ul>' if questions else ""
    source = "Claude read this spec. Pass and fail came from the catalog rules." if review.source == "claude" else "Prepared sample. Claude didn't run."
    return (
        f'<div class="sc-panel"><div class="sc-verdict"><div><div class="sc-kicker">{kicker}</div><h2>{escape(title)}</h2>{closest}</div>{chip}</div>'
        f'<div class="sc-counts"><div><b>{best.mandatory_fails}</b><span>Must-haves missed</span></div>'
        f'<div><b>{best.preferred_misses}</b><span>Preferred items missed</span></div>'
        f'<div><b>{best.reviews}</b><span>To review</span></div></div>{summary}{questions}'
        f'<p class="sc-small">{source}</p></div>'
    )


def type_box(equipment_type: str) -> None:
    name, text = TYPE_INFO[equipment_type]
    html(f'<div class="sc-type"><div class="sc-type-kicker">What this equipment is</div>'
         f'<b>{escape(name)}</b><p>{escape(text)}</p></div>')


def doc_html(text: str) -> str:
    """Shows spec text like a page in a document editor: title, headings, and full paragraphs."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    def is_heading(line: str) -> bool:
        return bool(re.match(r"^(\d+(\.\d+)*\.?|[A-Z]\.)\s+\S", line)) and len(line) < 70 and not line.endswith((".", ":", ";"))

    i, title = 1, lines[0] if lines else ""
    while (i < len(lines) and not is_heading(lines[i]) and not title.endswith(".")
           and not lines[i].lower().startswith("sample document") and len(lines[i]) < 40):
        title += " " + lines[i]
        i += 1
    parts, paragraph = [f"<h1>{escape(title)}</h1>"] if title else [], []

    def flush():
        if paragraph:
            joined = " ".join(paragraph)
            note = ' class="sc-docnote"' if joined.lower().startswith("sample document") else ""
            parts.append(f"<p{note}>{escape(joined)}</p>")
            paragraph.clear()

    for line in lines[i:]:
        if is_heading(line):
            flush()
            parts.append(f"<h2>{escape(line)}</h2>")
        else:
            paragraph.append(line)
            if line.lower().startswith("sample document"):
                flush()
    flush()
    return f'<div class="sc-docwrap"><article class="sc-docpage">{"".join(parts)}</article></div>'


def show_review(review: Review, spec_text: str, show_type: bool = True) -> None:
    band = "band-match" if review.recommended_id else "band-gap"
    with st.container(key=band):
        if show_type:
            type_box(review.equipment_type)
        label("Result")
        html(result_panel(review))

    with st.container(key="band-table"):
        label("Details")
        html('<div class="sc-h2">Requirement check</div>')
        names = {c.product_name: c for c in review.ranked}
        chosen = names[st.selectbox("Product", list(names))]
        counts = {s: sum(STATUS_LABELS[r.status] == s for r in chosen.results) for s in ("Fail", "Review", "Pass")}
        options = ["All", "Fail", "Review", "Pass"]
        shown = st.segmented_control(
            "Show",
            options,
            default="All",
            format_func=lambda s: f"{s} {counts[s] if s in counts else len(chosen.results)}",
        )
        html(compliance_table(chosen, shown or "All"))
        st.download_button(
            "Download CSV",
            to_csv(chosen),
            file_name=f"{chosen.product_id}-compliance.csv",
            mime="text/csv",
        )

    with st.container(key="band-products"):
        label("Costs")
        html('<div class="sc-h2">Material cost</div>')
        html(materials_table(review.ranked[0].product_id))
        price_inputs()
        price_charts()

    with st.container(key="band-spec"):
        label("Source")
        with st.expander("View original spec"):
            html(doc_html(spec_text))


TYPE_INFO = {
    "utility_service": [
        "Utility service section",
        "Where power from the power company comes into the site. It holds the main shutoff and the power meter."
    ],
    "transformer": [
        "Transformer",
        "Changes the voltage. It steps high voltage down to a lower voltage the site can use."
    ],
    "cable_bus": [
        "Cable bus",
        "Insulated cables held in a vented metal tray with a cover. It carries a lot of current between equipment, like from a transformer to switchgear."
    ],
    "iso_phase_bus": [
        "Iso phase bus",
        "Each of the three phases runs in its own metal tube. It carries very high current, like between a power plant's generator and its transformer."
    ],
    "non_seg_bus": [
        "Non-seg bus",
        "Metal bars for all three phases share one metal housing. It's a common way to connect a transformer to switchgear."
    ],
    "mv_switchgear": [
        "Medium-voltage switchgear",
        "Cabinets with breakers for power above 1,000 volts. They send power to different parts of the site and shut it off safely if something goes wrong."
    ],
    "lv_switchgear": [
        "Low-voltage switchgear",
        "Cabinets with breakers for power at 1,000 volts or less, like 480 volts. They feed equipment inside the building."
    ],
    "ups": [
        "UPS",
        "Battery backup. It keeps power on for a few minutes during an outage until the generators start."
    ],
    "server_rack": [
        "Server racks",
        "Frames that hold servers. These are built for AI computers that use a lot of power and need liquid cooling."
    ]
}

EQUIPMENT_INFO = {
    "Utility": "Where power from the power company enters the site. It has the main shutoff and the power meter.",
    "Transformer": "Changes the voltage. It usually steps high voltage down to a level the site can use.",
    "Bus": "Metal bars or cables inside a metal housing that carry a lot of current between equipment. Cable bus uses cables, iso phase bus gives each phase its own housing, and non-seg bus puts all three phases in one housing.",
    "Switchgear": "Large cabinets with breakers. They send power to different parts of the site and shut it off safely when something goes wrong.",
    "UPS": "Battery backup. It keeps power on for a few minutes during an outage until the generators start.",
    "Server racks": "Frames that hold the servers and computers that use the power."
}


def pick_equipment(name: str) -> None:
    """Clicking a card selects it. Clicking it again shows all equipment."""
    chosen = None if st.session_state.get("equipment") == name else name
    st.session_state["equipment"] = chosen


def equipment_panel() -> dict[str, str]:
    with st.container(key="band-path"):
        label("Equipment")
        html('<div class="sc-h2">What it covers</div>')
        chosen = st.session_state.get("equipment")
        columns = st.columns(len(EQUIPMENT))
        for column, (name, (icon, _)) in zip(columns, EQUIPMENT.items()):
            column.button(
                name,
                icon=icon,
                key=f"equipment-{name}",
                type="primary" if chosen == name else "secondary",
                width="stretch",
                on_click=pick_equipment,
                args=(name,),
            )
        if chosen:
            html(f'<div class="sc-panel" style="margin-top:14px"><b>{escape(chosen)}</b><p style="margin:4px 0 0">{escape(EQUIPMENT_INFO[chosen])}</p></div>')
        html('<p class="sc-small">Click equipment to see what it is and its sample specs. Click it again to see them all.</p>')
    if chosen:
        return EQUIPMENT[chosen][1]
    return {spec: file for _, specs in EQUIPMENT.values() for spec, file in specs.items()}


def claude_panel() -> None:
    html('<div class="sc-h2" style="margin-top:28px">Check your own spec</div>')
    typed_key = ""
    if not has_api_key():
        typed_key = st.text_input(
            "Claude API key",
            type="password",
            help="Used only for this visit. It isn't saved or stored on GitHub.",
        ).strip()
        if not typed_key:
            st.warning("Add your ANTHROPIC_API_KEY to the .env file, or paste a Claude API key above.")
            return
    if app_password() and not password_ok(st.text_input("Demo password", type="password")):
        st.info("Enter the demo password to use Claude.")
        return

    upload = st.file_uploader("Spec PDF", type="pdf")
    if upload and st.button("Run review", type="primary"):
        if not review_counter().take(daily_limit()):
            st.warning("Today's review limit has been reached. Please try again tomorrow.")
            return
        try:
            spec_text = read_pdf(upload.getvalue())
            with st.spinner(""):
                client = Anthropic(api_key=typed_key) if typed_key else None
                st.session_state["review"] = SpecAgent(catalog(), client=client).run(spec_text)
                st.session_state["review_text"] = spec_text
                st.session_state["showing"] = "claude"
        except (SpecFileError, AgentError) as error:
            st.error(str(error))
        except APIError as error:
            st.error(f"The Claude API returned an error: {error}")


html(CSS)
html(HEADER)
sample_names = equipment_panel()

def show_samples() -> None:
    st.session_state["showing"] = "sample"


with st.container(key="band-demo"):
    label("Demo")
    html('<div class="sc-h2">Pick a sample spec</div>')
    names = list(sample_names)
    name = st.segmented_control(
        "Sample spec",
        names,
        default=names[0],
        key=f"sample-{st.session_state.get('equipment')}",
        on_change=show_samples,
        label_visibility="collapsed",
    ) or names[0]
    sample = sample_names[name]
    sample_review, sample_text = saved_review(sample)
    type_box(sample_review.equipment_type)
    st.download_button(
        "Download this sample PDF",
        (SAMPLES / f"{sample}.pdf").read_bytes(),
        file_name=f"{sample}.pdf",
        mime="application/pdf",
    )
    claude_panel()

if st.session_state.get("showing") == "claude" and "review" in st.session_state:
    show_review(st.session_state["review"], st.session_state["review_text"])
else:
    show_review(sample_review, sample_text, show_type=False)

html(FOOTER)
