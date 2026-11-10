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
from speccheck.models import CheckResult, ProductCheck, Review, SpecRequirements
from speccheck.pdf import SpecFileError, read_pdf
from speccheck.review import build_review, to_csv
from speccheck.settings import DailyCounter, app_password, daily_limit, has_api_key, password_ok
from speccheck.theme import CSS, FOOTER, HEADER

ROOT = Path(__file__).parent
SAMPLES = ROOT / "data" / "samples"
EQUIPMENT = {
    "Utility": (":material/electric_bolt:", {"Mill Creek: utility service": "mill_creek_utility"}),
    "Transformer": (":material/settings_input_component:", {"Summit: 30 MVA transformer": "summit_transformer"}),
    "Bus": (":material/view_stream:", {
        "Ridgeline: cable bus": "ridgeline_cable_bus",
        "Lakeshore: iso phase bus": "lakeshore_iso_bus",
        "Prairie: non-seg bus": "prairie_non_seg",
    }),
    "Switchgear": (":material/dashboard:", {
        "Project Red Oak: 13.8 kV data center": "red_oak_mv",
        "Harbor Colo: 480 V service": "harbor_lv",
        "High Desert: 34.5 kV outdoor": "high_desert_mv",
    }),
    "UPS": (":material/battery_charging_full:", {"Orion: 1.5 MW UPS": "orion_ups"}),
    "Server racks": (":material/dns:", {"Atlas: AI server racks": "atlas_server_racks"}),
}
STATUS_LABELS = {"PASS": "Pass", "FAIL": "Fail", "REVIEW": "Review"}
SHORT_NAMES = {
    "Rated maximum voltage": "Max voltage",
    "Impulse withstand (BIL)": "BIL",
    "Continuous current": "Current",
    "Short-circuit rating": "Short circuit",
    "Ambient temperature": "Ambient temp",
    "Site altitude": "Altitude",
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


def required_text(result: CheckResult) -> str:
    text = re.sub(r"^at least (.*)$", r"\1 min", result.required)
    return re.sub(r"^at most (.*)$", r"\1 max", text)


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
    show_note = any(r.note for r in check.results)
    note_head = "<th>Note</th>" if show_note else ""
    rows = []
    for r in results:
        note = f"<td>{escape(note_text(r))}</td>" if show_note else ""
        product = "—" if r.product_value == "Not checked" else r.product_value
        rows.append(
            f'<tr><td><span class="sc-chip {r.status}">{STATUS_LABELS[r.status]}</span></td>'
            f"<td>{escape(r.requirement.section)}</td><td>{escape(item_name(r))}</td>"
            f'<td>{"Must have" if r.requirement.mandatory else "Preferred"}</td>'
            f'<td class="sc-num">{escape(required_text(r))}</td><td class="sc-num">{escape(product)}</td>'
            f'<td class="sc-quote">{escape(r.requirement.source_quote)}</td>{note}</tr>'
        )
    body = "".join(rows) or '<tr><td colspan="8">No items with this status.</td></tr>'
    return (
        '<div class="sc-scroll"><table><thead><tr><th>Status</th><th>Section</th><th>Item</th><th>Priority</th>'
        f"<th>Required</th><th>Product</th><th>Spec wording</th>{note_head}</tr></thead><tbody>{body}</tbody></table></div>"
    )


def products_table(review: Review) -> str:
    rows = "".join(
        f'<tr><td>{escape(c.product_name)}</td><td class="sc-num">{c.mandatory_fails}</td>'
        f'<td class="sc-num">{c.preferred_misses}</td><td class="sc-num">{c.reviews}</td></tr>'
        for c in review.ranked
    )
    return (
        '<div class="sc-scroll small"><table><thead><tr><th>Product</th><th>Must-haves missed</th>'
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


def show_review(review: Review, spec_text: str) -> None:
    band = "band-match" if review.recommended_id else "band-gap"
    with st.container(key=band):
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
        label("Compare")
        html('<div class="sc-h2">Product comparison</div>')
        html(products_table(review))

    with st.container(key="band-spec"):
        label("Source")
        with st.expander("View original spec"):
            html(f'<pre class="sc-spec">{escape(spec_text)}</pre>')


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
        html('<p class="sc-small">Click equipment to see its sample specs. Click it again to see them all.</p>')
    if chosen:
        return EQUIPMENT[chosen][1]
    return {spec: file for _, specs in EQUIPMENT.values() for spec, file in specs.items()}


def claude_panel() -> None:
    html('<div class="sc-h2">Check your own spec</div>')
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
    st.caption("Your text is sent to Claude and uses API credits. Don't upload confidential documents.")
    if upload and st.button("Run review", type="primary"):
        if not review_counter().take(daily_limit()):
            st.warning("Today's review limit has been reached. Please try again tomorrow.")
            return
        try:
            spec_text = read_pdf(upload.getvalue())
            with st.spinner("Claude is reading the spec. This can take a minute..."):
                client = Anthropic(api_key=typed_key) if typed_key else None
                st.session_state["review"] = SpecAgent(catalog(), client=client).run(spec_text)
                st.session_state["review_text"] = spec_text
        except (SpecFileError, AgentError) as error:
            st.error(str(error))
        except APIError as error:
            st.error(f"The Claude API returned an error: {error}")


html(CSS)
html(HEADER)
sample_names = equipment_panel()

with st.container(key="band-demo"):
    label("Demo")
    mode = st.segmented_control(
        "Mode",
        ["Sample specs", "Check your own spec"],
        default="Sample specs",
        label_visibility="collapsed",
    ) or "Sample specs"
    if mode == "Sample specs":
        html('<div class="sc-h2">Pick a sample spec</div>')
        names = list(sample_names)
        name = st.segmented_control(
            "Sample spec",
            names,
            default=names[0],
            key=f"sample-{st.session_state.get('equipment')}",
            label_visibility="collapsed",
        ) or names[0]
        sample = sample_names[name]
        st.download_button(
            "Download this sample PDF",
            (SAMPLES / f"{sample}.pdf").read_bytes(),
            file_name=f"{sample}.pdf",
            mime="application/pdf",
        )
    else:
        claude_panel()

if mode == "Sample specs":
    show_review(*saved_review(sample))
elif "review" in st.session_state:
    show_review(st.session_state["review"], st.session_state["review_text"])

html(FOOTER)
