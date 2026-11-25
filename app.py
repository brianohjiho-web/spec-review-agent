"""SpecCheck AI web app. Run it with: streamlit run app.py"""
import json
import os
import re
from html import escape
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from anthropic import Anthropic, APIError
from dotenv import load_dotenv

from speccheck.agent import AgentError, SpecAgent
from speccheck import api_catalog
from speccheck.catalog import DEFAULT_CATALOG, PUBLIC_CATALOG, load_catalog
from speccheck.checks import GROUP_OF, GROUPS, RULES
from speccheck.metals import CHARTS, ENTERED, LB_PER_METRIC_TON, LIVE, latest_prices, material_cost, per_lb
from speccheck.models import CheckResult, ProductCheck, Review, SpecRequirements
from speccheck.pdf import SpecFileError, read_pdf, read_pdfs
from speccheck.review import build_review, to_pdf
from speccheck.settings import DailyCounter, app_password, daily_limit, has_api_key, password_ok
from speccheck.questions import make_questions
from speccheck.theme import CSS, HEADER, REVEAL_JS, icon, section_head

ROOT = Path(__file__).parent
SAMPLES = ROOT / "data" / "samples"
EXAMPLES = ROOT / "data" / "examples"
ORIGINALS = ROOT / "data" / "originals"
# The unedited public specs each example is based on. Downloads give these.
ORIGINAL_FILES = {
    "example_va_mv_switchgear": "VA_26_13_13.pdf",
    "example_va_lv_switchgear": "VA_26_23_00.pdf",
    "example_university_lv_switchgear": "NU_26_23_00_low_voltage_switchgear.pdf",
    "example_va_ups": "VA_26_33_53.pdf",
    "example_university_ups": "WSU_26_33_53_static_UPS.pdf",
}
EXAMPLE_FILES = [
    ("example_va_mv_switchgear", "mv", "MV switchgear", "15 kV", "26 13 13", "Veterans Affairs"),
    ("example_va_lv_switchgear", "lv", "LV switchgear", "480 V", "26 23 00", "Veterans Affairs"),
    ("example_university_lv_switchgear", "lv", "LV switchgear", "480/277 V", "26 23 00", "Northwestern Univ."),
    ("example_va_ups", "ups", "UPS", "500 kVA", "26 33 53", "Veterans Affairs"),
    ("example_university_ups", "ups", "UPS", "100 kVA", "26 33 53", "Washington State Univ."),
]
EXAMPLE_CSS = """<style>
.sc-ex-head{font-size:.86rem;color:#5f6c76;margin:0 0 8px}.sc-ex-head b{color:#1d2730;margin-right:4px}.sc-sub{color:#5f6c76;font-size:.95rem;margin:-4px 0 12px}.sc-words{text-align:right;font-size:.8rem;color:#5f6c76;margin:-6px 0 4px}
[data-testid="stFileUploaderDropzoneInstructions"]{display:none!important}
html:root body .st-key-pasted-spec{background:#f1f3f4;padding:18px 12px;border-radius:8px}
html:root body .st-key-pasted-spec textarea{font-family:"Times New Roman",Times,serif!important;font-size:12pt!important;line-height:1.55!important;color:#1a1a1a!important;background:#fff!important;max-width:760px;margin:0 auto;padding:40px 56px!important;border:0!important;border-radius:2px!important;box-shadow:0 1px 3px rgba(60,64,67,.3),0 4px 8px rgba(60,64,67,.15)!important;text-align:left}
html:root body .st-key-pasted-spec [data-baseweb="textarea"],html:root body .st-key-pasted-spec [data-baseweb="base-input"]{background:transparent!important;border:0!important;display:block;max-width:760px;margin:0 auto}
.st-key-exband{background:#f6f7f7;border:1px solid #e1e5e8;border-radius:12px;padding:14px 16px;margin:12px 0 14px}
[class*="st-key-exc-"]{--ex:#2f6db0;position:relative;border:1px solid #dde2e6;border-left:3px solid var(--ex);border-radius:9px;background:#fff;padding:9px 34px 9px 12px;gap:0!important;}
[class*="st-key-exc-lv"]{--ex:#1f8a7a}[class*="st-key-exc-ups"]{--ex:#c47a12}
[class*="st-key-exc-"]:hover{transform:translateY(-1px);border-color:color-mix(in srgb,var(--ex) 45%,#dde2e6);border-left-color:var(--ex);box-shadow:0 6px 16px -10px color-mix(in srgb,var(--ex) 60%,transparent)}
[class*="st-key-exc-"]:has(.sc-ex.on){border-color:var(--ex);border-width:2px 2px 2px 5px;background:color-mix(in srgb,var(--ex) 12%,#fff);box-shadow:0 0 0 4px color-mix(in srgb,var(--ex) 22%,transparent),0 8px 18px -10px color-mix(in srgb,var(--ex) 70%,transparent)}
[class*="st-key-exc-"]:has(.sc-ex.on) .l1 b{color:var(--ex)}
[class*="st-key-exc-"] [data-testid="stElementContainer"],[class*="st-key-exc-"] [data-testid="stMarkdownContainer"],[class*="st-key-exc-"] [data-testid="stMarkdown"]{margin:0!important;height:auto!important;overflow:visible!important}
.sc-ex{display:grid;gap:1px;line-height:1.35;padding:1px 0 2px}
.sc-ex .l1{display:flex;align-items:baseline;gap:5px;white-space:nowrap;overflow:hidden}
.sc-ex .l1 b{font-size:.9rem;font-weight:600;color:#1d2730}
.sc-ex .l1 span{font-size:.68rem;color:#5f6c76;overflow:hidden;text-overflow:ellipsis}
.sc-ex .o{font-size:.66rem;color:#5f6c76;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.sc-ex .o b{color:var(--ex);font-weight:700;margin-right:4px}
.sc-ex .s{font-family:ui-monospace,Consolas,monospace;font-size:.62rem;color:#5f6c76}
[class*="st-key-exc-"] [class*="st-key-try-"]{position:absolute!important;inset:0;z-index:1;width:auto!important}
[class*="st-key-exc-"] [class*="st-key-try-"] *{width:100%!important;height:100%!important}
html:root body [class*="st-key-exc-"] [class*="st-key-try-"] button{opacity:0!important;cursor:pointer!important;min-height:0!important;border:0!important;background:transparent!important}
[class*="st-key-exc-"] [class*="st-key-pdf-"]{position:absolute!important;top:50%;right:6px;transform:translateY(-50%);z-index:2;width:auto!important}
html:root body [class*="st-key-exc-"] [class*="st-key-pdf-"] button{min-height:26px!important;width:26px!important;padding:0!important;border-radius:7px!important;border:1px solid transparent!important;background:transparent!important;color:#5f6c76!important;font-size:.9rem!important;text-transform:none!important;letter-spacing:0!important}
html:root body [class*="st-key-exc-"] [class*="st-key-pdf-"] button:hover{color:var(--ex)!important;border-color:color-mix(in srgb,var(--ex) 40%,#dde2e6)!important;background:color-mix(in srgb,var(--ex) 8%,#fff)!important}
</style>"""
EQUIPMENT = {
    "Utility": (":material/electric_bolt:", {"Utility service": "mill_creek_utility"}),
    "Transformer": (":material/settings_input_component:", {"Transformer": "summit_transformer"}),
    "Bus": (":material/view_stream:", {
        "Cable bus": "ridgeline_cable_bus",
        "Iso phase bus": "lakeshore_iso_bus",
        "Non-seg bus": "prairie_non_seg",
    }),
    "Switchgear": (":material/dashboard:", {"Switchgear": None}),
    "UPS": (":material/battery_charging_full:", {"UPS": "orion_ups"}),
    "Server racks": (":material/dns:", {"Server racks": "atlas_server_racks"}),
}
# Examples built from real public specs. Picked in a second row like switchgear.
REAL_SPECS = {
    "MV switchgear 15 kV · VA": "example_va_mv_switchgear",
    "LV switchgear 480 V · VA": "example_va_lv_switchgear",
    "LV switchgear 480/277 V · Northwestern": "example_university_lv_switchgear",
    "UPS 500 kVA · VA": "example_va_ups",
    "UPS 100 kVA · Washington State": "example_university_ups",
}
# The switchgear samples share one button; the voltage is picked in a second row.
SWITCHGEAR = {
    "480 V · indoor": "harbor_lv",
    "600 V · outdoor": "maple_600v_lv",
    "13.8 kV · indoor": "red_oak_mv",
    "34.5 kV · outdoor": "high_desert_mv",
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
    for name in ("ANTHROPIC_API_KEY", "APP_PASSWORD", "DAILY_REVIEW_LIMIT", "SPECCHECK_MODEL",
                 "PRODUCT_API_URL", "PRODUCT_API_KEY", "PRODUCT_API_AUTH", "CATALOG_FILE"):
        if name in secrets and not os.getenv(name):
            os.environ[name] = str(secrets[name])


load_streamlit_secrets()


CATALOGS = {"Public datasheets": PUBLIC_CATALOG, "Demo catalog with prices": DEFAULT_CATALOG}


@st.cache_data
def read_catalog(path: str) -> list[dict]:
    return load_catalog(path)


@st.cache_data(ttl=3600, show_spinner="Loading products from the company API...")
def read_api_catalog() -> list[dict]:
    return api_catalog.load_from_api()


def catalog() -> list[dict]:
    """Where products come from, first match wins:
    1. A company product API, if PRODUCT_API_URL is set (refreshed every hour).
    2. A saved catalog file, if CATALOG_FILE is set (for example data/catalog_company.json).
    3. Ratings from public datasheets (the default).
    Tests can swap in the fixed demo catalog to get stable results."""
    if "catalog_choice" in st.session_state:
        return read_catalog(str(CATALOGS[st.session_state["catalog_choice"]]))
    if api_catalog.enabled():
        try:
            return read_api_catalog()
        except Exception as err:  # Keep the app usable if their API is down.
            st.warning(f"Couldn't load the company product API ({type(err).__name__}). Using public datasheets instead.")
    if os.getenv("CATALOG_FILE"):
        return read_catalog(os.environ["CATALOG_FILE"])
    return read_catalog(str(PUBLIC_CATALOG))


@st.cache_resource
def review_counter() -> DailyCounter:
    return DailyCounter()


@st.cache_data
def download_file(sample: str) -> Path:
    """The PDF to hand out: the original public spec for real-spec examples, else the sample itself."""
    original = ORIGINALS / ORIGINAL_FILES.get(sample, "")
    return original if sample in ORIGINAL_FILES and original.exists() else sample_folder(sample) / f"{sample}.pdf"


@st.cache_data
def file_bytes(path: Path) -> bytes:
    return path.read_bytes()


def sample_folder(sample: str) -> Path:
    return EXAMPLES if (EXAMPLES / f"{sample}.pdf").exists() else SAMPLES


@st.cache_data(show_spinner=False)
def saved_spec(sample: str) -> tuple[dict, str]:
    folder = sample_folder(sample)
    text = read_pdf((folder / f"{sample}.pdf").read_bytes())
    data = json.loads((folder / f"{sample}.requirements.json").read_text(encoding="utf-8"))
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


def product_facts(product: dict, short: bool = False) -> str:
    """Voltage, current or power, and phases for one catalog product, plus its source if public."""
    facts = []
    volts = product.get("voltage_kv")
    if volts is not None:
        facts.append(("Voltage", f"{volts * 1000:g} V" if volts < 1 else f"{volts:g} kV"))
    for key, unit in (("bus_current_a", "A"), ("power_kva", "kVA"), ("power_kw", "kW"), ("rack_units", "U")):
        if product.get(key) is not None:
            facts.append(("Current" if key == "bus_current_a" else "Rating", f"{product[key]:g} {unit}"))
    if product.get("phases"):
        facts.append(("Phases", " or ".join(str(p) for p in product["phases"])))
    if short:
        return ", ".join(value for _, value in facts) or "ratings in source"
    text = " · ".join(f"<b>{label}</b> {value}" for label, value in facts)
    if product.get("source_url"):
        source = f'<a href="{escape(product["source_url"])}" target="_blank" rel="noopener">{escape(product["maker"])} source page</a>'
        text = f'{text} · {source}' if text else source
        text += f'<br><span class="sc-small">{escape(product.get("source_note", ""))}</span>'
    return text

RAIL = """<nav class="sc-rail" aria-label="Sections"><a target="_self" href="#top" title="Top"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/></svg><span>Top</span></a><a target="_self" href="#sec-samples" title="Sample specs"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg><span>Sample specs</span></a><a target="_self" href="#sec-live" title="Check your own spec"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 16V4"/><path d="m7 9 5-5 5 5"/><path d="M5 20h14"/></svg><span>Check your own spec</span></a><a target="_self" href="#sec-result" title="Best match"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="9" r="6"/><path d="m8.5 14-1.5 7 5-3 5 3-1.5-7"/></svg><span>Best match</span></a><a target="_self" href="#sec-check" title="Requirement check"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/></svg><span>Requirement check</span></a><a target="_self" href="#sec-compare" title="Compare products"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M9 4v16M15 4v16"/></svg><span>Compare products</span></a><a target="_self" href="#sec-cost" title="Material cost"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m3 17 6-6 4 4 8-8"/><path d="M15 7h6v6"/></svg><span>Material cost</span></a><a target="_self" href="#sec-questions" title="Questions to ask"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12Z"/></svg><span>Questions to ask</span></a><a target="_self" href="#sec-spec" title="Original spec"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8Z"/><path d="M14 3v5h5M9 13h6M9 17h6"/></svg><span>Original spec</span></a></nav>"""

JUMP = """<details class="sc-jump"><summary>Sections</summary><nav>
<a href="#sec-samples">Sample specs</a><a href="#sec-check">Requirement check</a>
<a href="#sec-compare">Compare products</a><a href="#sec-cost">Material cost</a><a href="#sec-questions">Questions to ask</a><a href="#sec-spec">Original spec</a></nav></details>"""


def required_text(result: CheckResult) -> str:
    text = re.sub(r"^at least (.*)$", r"\1 min", result.required)
    return usd(re.sub(r"^at most (.*)$", r"\1 max", text))


def item_name(result: CheckResult) -> str:
    rule = RULES.get(result.requirement.parameter)
    return SHORT_NAMES.get(rule.label, rule.label) if rule else "Other"


NOT_LISTED = '<span class="sc-na">—</span>'


def why(result: CheckResult) -> str:
    text = reason(result)
    return f'<div class="sc-why">{escape(text)}</div>' if text else ""


def reason(result: CheckResult) -> str:
    """A short plain reason for a failed or review row. Pass rows need none."""
    need = usd(result.required.replace("at least ", "").replace("at most ", ""))
    note = result.note
    if result.status == "PASS":
        return ""
    if result.status == "FAIL":
        if result.required.startswith("at least"):
            return f"Below the {need} minimum"
        if result.required.startswith("at most"):
            return f"Over the {need} limit"
        return f"Doesn't offer {need}"
    for key, text in (
        ("source quote was not found", "Words not found in the spec. Check how it was read."),
        ("value was not found in the source quote", "Number doesn't match the spec text"),
        ("outside the automatic checks", "The tool can't check this. An engineer should read it."),
        ("public page", "Not mentioned on the maker's page"),
        ("no value", "Not listed in the product data"),
        ("Unknown unit", "Unknown unit. Check by hand."),
        ("not one the tool knows", "Unknown value. Check by hand."),
        ("No required value", "Spec has no clear value. Ask the customer."),
    ):
        if key in note:
            return text
    return note or "Check by hand"

def compare_table(review: Review) -> str:
    """Every product of this type side by side, one row per spec item."""
    products = review.ranked
    makers = {p["id"]: p.get("maker", "") for p in catalog()}
    mine = review.source == "claude"  # An uploaded PDF gets its own column.
    head = "<th>Spec item</th>"
    if mine:
        head += '<th class="mine"><div class="sc-cmp-maker">Your PDF</div><div class="sc-cmp-name">Uploaded file</div></th>'
    for n, c in enumerate(products):
        if c.mandatory_fails:
            summary, tone = f"{c.mandatory_fails} fail · {c.reviews} to check", "bad"
        elif c.reviews:
            summary, tone = f"No fails · {c.reviews} to check", "warn"
        else:
            summary, tone = "Meets all", "ok"
        maker = makers.get(c.product_id, "")
        name = c.product_name.replace(maker, "").strip() if maker else c.product_name
        tag = '<div class="sc-cmp-tag">Best match</div>' if n == 0 else ""
        head += (f'<th class="{"best" if n == 0 else ""}"><div class="sc-cmp-maker">{escape(maker)}</div>'
                 f'<div class="sc-cmp-name">{escape(name or c.product_name)}</div>'
                 f'<div class="sc-cmp-sum {tone}">{summary}</div>{tag}</th>')
    rows = ""
    for k, first in enumerate(products[0].results if products else []):
        cells = ""
        for n, c in enumerate(products):
            r = c.results[k]
            if r.status == "REVIEW" and (r.product_value in ("Not checked", "Not listed") or r.requirement.parameter == "features"):
                body = NOT_LISTED
            else:
                mark = {"PASS": "✓", "FAIL": "✗", "REVIEW": "?"}[r.status]
                body = f'<span class="sc-mk {r.status}">{mark}</span>{escape(usd(r.product_value))}'
            tip = f' title="{escape(reason(r))}"' if reason(r) else ""
            cells += f'<td class="c-{r.status}{" best" if n == 0 else ""}"{tip}>{body}</td>'
        need = "" if mine else f'<div class="sc-ci-need">{escape(required_text(first))}</div>'
        pdf = f'<td class="mine">{escape(usd(first.required.replace("at least ", "").replace("at most ", "")))}</td>' if mine else ""
        rows += f'<tr><th><div class="sc-ci-name">{escape(item_name(first))}</div>{need}</th>{pdf}{cells}</tr>'
    return (
        '<p class="sc-small"><span class="sc-mk PASS">✓</span> meets &nbsp; <span class="sc-mk FAIL">✗</span> doesn\'t meet &nbsp; '
        '<span class="sc-mk REVIEW">?</span> needs a look &nbsp; <span class="sc-na">—</span> not listed</p>'
        f'<div class="sc-scroll"><table class="sc-cmp"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'
    )

def compliance_table(check: ProductCheck, status: str) -> str:
    """A compliance matrix with rows grouped by topic."""
    numbered = list(enumerate(check.results, 1))
    shown = [(n, r) for n, r in numbered if status == "All" or STATUS_LABELS[r.status] == status]
    rows = []
    count = 0
    for group in [*GROUPS, "Other"]:
        items = [(n, r) for n, r in shown if GROUP_OF.get(r.requirement.parameter, "Other") == group]
        if not items:
            continue
        passed = sum(r.status == "PASS" for _, r in items)
        rows.append(f'<tr class="sc-grp" data-g="{group}"><td colspan="6">{group}<span>{passed} of {len(items)} pass</span></td></tr>')
        for _, r in items:
            count += 1
            n = count
            product = NOT_LISTED if r.product_value in ("Not checked", "Not listed") else escape(usd(r.product_value))
            pref = '<span class="sc-pref">Preferred</span>' if not r.requirement.mandatory else ""
            section = f'<span class="sc-sec">Section {escape(r.requirement.section)}</span>' if r.requirement.section else ""
            rows.append(
                f'<tr class="sc-row-{r.status}"><td class="sc-num">{n}</td>'
                f'<td><div class="sc-name">{escape(item_name(r))}{pref}</div></td>'
                f'<td>{escape(required_text(r))}</td><td>{product}</td>'
                f'<td><span class="sc-chip {r.status}">{STATUS_LABELS[r.status]}</span>{why(r)}</td>'
                f'<td class="sc-ref">{section}<span class="sc-quote">“{escape(r.requirement.source_quote)}”</span></td></tr>'
            )
    body = "".join(rows) or '<tr><td colspan="6">No items with this status.</td></tr>'
    return (
        f'<div class="sc-scroll"><table class="sc-matrix"><thead><tr><th>#</th><th>Requirement</th>'
        f"<th>Spec needs</th><th>Product has</th><th>Result</th><th>Spec reference</th></tr></thead>"
        f"<tbody>{body}</tbody></table></div>"
    )

def money(value) -> str:
    return "—" if value is None else f"${value:,.0f}"


@st.cache_data(ttl=12 * 60 * 60, show_spinner=False)
def metal_prices() -> dict:
    return latest_prices()


CALCULATOR = {**{k: (v, "lb") for k, v in LIVE.items()}, **ENTERED}


def entered_prices() -> dict:
    return {}  # No typed prices: FRED for metals, default prices for the rest.


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

    def bar_row(name, value, color, extra=""):
        return (f'<div class="sc-split-row"{extra}><span>{escape(name)}</span>'
                f'<div class="sc-split-bar"><span style="width:{max(0.5, value / price * 100):.2f}%;background:{color}"></span></div>'
                f'<span class="sc-split-num">{money(value)}</span><span class="sc-split-num" style="color:#566575">{pct(value)}</span></div>')

    by_name = {r["name"]: r for r in rows}
    body = ""
    for name, _ in CALCULATOR.values():
        r = by_name.get(name)
        if r and r["cost"]:
            body += bar_row(name, r["cost"], "#0b6e76")
        else:
            label = "No price" if r else "Not used"
            body += (f'<div class="sc-split-row" style="color:#566575"><span>{name}</span><div class="sc-split-bar"></div>'
                     f'<span class="sc-split-num" style="font-size:.8rem">{label}</span><span class="sc-split-num">—</span></div>')
    body += bar_row("Other costs (labor, parts, overhead)", max(0, price - total), "#566575",
                    ' style="border-top:1px solid #dfe5ea;padding-top:8px"')
    return f'<div class="sc-split"><b>Product price: {money(price)} = 100%</b>{body}</div>'


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
            cards += (f'<div class="sc-trend" data-m="{name}"><div class="sc-tag" style="font-weight:600">{name}</div>'
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
            f'<div class="sc-trend" data-m="{name}"><div class="sc-tag" style="font-weight:600">{name}</div>{sub}'
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
    """Best match card: name, verdict, key facts, and a small pass score on the right."""
    best = review.ranked[0]
    match = bool(review.recommended_id)
    kind = TYPE_INFO[review.equipment_type][0]
    kicker = f'{"Best match" if match else "No full match"} · {kind}'
    title = best.product_name if match else "No product meets every must-have item"
    if match and best.reviews:
        verdict, tone = f"Meets every required item. {best.reviews} still need a check", "warn"
    elif match:
        verdict, tone = "Meets every must-have item", "ok"
    else:
        verdict, tone = f"{best.mandatory_fails} must-have item{'s' if best.mandatory_fails != 1 else ''} not met", "bad"
    closest = "" if match else f'<p class="sc-closest">Closest option: {escape(best.product_name)}</p>'
    product = next((p for p in catalog() if p["id"] == best.product_id), {})
    facts = product_facts(product, short=True)
    summary = f"<p>{escape(review.summary)}</p>" if review.summary else ""
    questions = "".join(f"<li>{escape(q)}</li>" for q in review.customer_questions)
    questions = f'<p class="sc-small">Questions for the customer:</p><ul>{questions}</ul>' if questions else ""
    source = "Claude read this spec. Pass and fail came from the catalog rules." if review.source == "claude" else "Saved sample result. Upload your own spec to run Claude live."
    total = len(best.results)
    counts = {s: sum(r.status == s for r in best.results) for s in ("PASS", "REVIEW", "FAIL")}
    bar = "".join(f'<span class="sc-bar-{s}" style="flex:{counts[s]}"></span>' for s in counts if counts[s])
    score = (f'<aside class="sc-score"><div class="sc-score-lbl">Passed</div>'
             f'<div class="sc-score-num"><b>{counts["PASS"]}</b> of {total}</div><div class="sc-bar">{bar}</div>'
             f'<div class="sc-score-det"><span class="{"bad" if counts["FAIL"] else ""}">{counts["FAIL"]} fail</span>'
             f'<span class="{"warn" if counts["REVIEW"] else ""}">{counts["REVIEW"]} to check</span></div></aside>')
    return (
        f'<div class="sc-res-row"><div class="sc-panel"><div class="sc-kicker">{kicker}</div><h2>{escape(title)}</h2>'
        f'<p class="sc-verdict {tone}">{verdict}</p>{closest}<p class="sc-facts">{escape(facts)}</p>'
        f'{summary}{questions}<p class="sc-small">{source}</p></div>{score}</div>'
    )

def type_box(equipment_type: str) -> None:
    name, text = TYPE_INFO[equipment_type]
    html(f'<div class="sc-type"><div class="sc-type-kicker">About this equipment</div>'
         f'<b>{escape(name)}</b><p>{escape(text)}</p></div>')


PAGE_NUMBER = re.compile(r"^\d\d \d\d \d\d ?- ?(\d+)$")
ITEM = re.compile(r"^(//)?([A-Z]\.|\d+\.|[a-z]\.|\d+\))\s+(.*)$")
DOTTED = re.compile(r"^(\S.*?)\.{4,}(.*)$")
END_MARKS = ("END OF SECTION", "---END---")


def spec_lines(text: str) -> list[str]:
    """Spec text lines. Each page header becomes a "\\f<page label>" marker; other repeated header lines are dropped."""
    lines = []
    for line in (re.sub(r"\s+", " ", line).strip() for line in text.splitlines()):
        if not line or line == "Issued for Construction" or re.match(r"^\d\d-\d\d-\d\d$", line):
            continue
        number = PAGE_NUMBER.match(line)
        lines.append(f"\f{line}" if number else line)
    start = next((i for i, line in enumerate(lines) if line.startswith("SECTION ")), 0)
    lines = lines[start:]
    while lines and lines[0].startswith("\f"):
        lines.pop(0)
    return lines


@st.cache_data(show_spinner=False)
def doc_html(text: str) -> str:
    """Shows spec text like a printed spec: title, notes, parts, articles, nested items, and page breaks."""
    lines = spec_lines(text)

    def level(marker: str) -> int:
        return 1 if marker[0].isupper() else 2 if marker[0].isdigit() and marker.endswith(".") else 4 if marker.endswith(")") else 3

    def is_heading(line: str) -> bool:
        if re.match(r"^(//)?PART \d+\s*-", line) or line in END_MARKS:
            return True
        return bool(re.match(r"^(//)?\d+\.\d+(\.\d+)*\.?\s+\S", line)) and len(line) < 80 and line.split(maxsplit=1)[1][:1].isupper() and not line.endswith((".", ":", ";"))

    def starts_block(line: str) -> bool:
        return is_heading(line) or line.startswith("\f") or bool(ITEM.match(line)) or line.startswith("SPEC WRITER NOTE")

    i, title = 1, [lines[0]] if lines else []
    while (i < len(lines) and not starts_block(lines[i]) and not title[-1].endswith(".")
           and not lines[i].lower().startswith("sample document") and len(lines[i]) < 60):
        title.append(lines[i])
        i += 1
    parts = [f"<h1>{'<br>'.join(escape(t) for t in title)}</h1>"] if title else []
    kind, buffer = "", []

    def flush():
        if buffer:
            joined = " ".join(buffer)
            if kind == "note":
                parts.append(f'<p class="sc-note">{escape(joined)}</p>')
            elif kind == "docnote":
                parts.append(f'<p class="sc-docnote">{escape(joined)}</p>')
            elif kind == "ref":
                code, _, rest = joined.partition("\x00")
                parts.append(f'<p class="sc-ref"><span>{escape(code)}</span><span>{escape(rest)}</span></p>')
            elif kind.startswith("item"):
                parts.append(f'<p class="sc-item sc-l{kind[4:]}">{escape(joined)}</p>')
            else:
                parts.append(f"<p>{escape(joined)}</p>")
            buffer.clear()

    for line in lines[i:]:
        if line.startswith("\f"):
            flush()
            kind = ""
            parts.append(f'<div class="sc-pg"><span>{escape(line[1:])}</span></div>')
        elif is_heading(line):
            flush()
            kind = ""
            tag = "h2" if "PART " in line[:8] else "h4" if line in END_MARKS else "h3"
            parts.append(f"<{tag}>{escape(line)}</{tag}>")
        elif line.startswith("SPEC WRITER NOTE"):
            flush()
            kind = "note"
            buffer.append(line)
        elif line.lower().startswith("sample document"):
            flush()
            kind = "docnote"
            buffer.append(line)
            flush()
            kind = ""
        elif kind.startswith("note") and not (ITEM.match(line) or DOTTED.match(line)):
            buffer.append(line)
        elif DOTTED.match(line):
            flush()
            kind = "ref"
            code, rest = DOTTED.match(line).groups()
            buffer.append(f"{code}\x00{rest.strip()}")
        elif ITEM.match(line):
            flush()
            kind = f"item{level(ITEM.match(line).group(2))}"
            buffer.append(line)
        else:
            if kind == "ref" and buffer and "\x00" in buffer[0]:
                buffer[0] += " " + line
            else:
                buffer.append(line)
    flush()
    return f'<div class="sc-docwrap"><article class="sc-docpage">{"".join(parts)}</article></div>'


def show_review(review: Review, spec_text: str, show_type: bool = True) -> None:
    band = "band-match" if review.recommended_id else "band-gap"
    with st.container(key=band):
        html('<span class="sc-anchor" id="sec-result"></span>')
        label("Result")
        html(result_panel(review))

    with st.container(key="band-table"):
        html('<span class="sc-anchor" id="sec-check"></span>')
        label("Details")
        html(section_head("check", "Requirement check", 1) +
             '<p class="sc-legend"><span class="sc-chip PASS">Pass</span> meets the spec '
             '<span class="sc-chip FAIL">Fail</span> product doesn\'t '
             '<span class="sc-chip REVIEW">Review</span> not enough info, check by hand</p>')
        names = {c.product_name: c for c in review.ranked}
        by_name = {p["name"]: p for p in catalog()}
        pick_col, show_col = st.columns([3, 2], vertical_alignment="bottom")
        picked = pick_col.selectbox("Product", list(names), format_func=lambda n: n)
        chosen = names[picked]
        counts = {s: sum(STATUS_LABELS[r.status] == s for r in chosen.results) for s in ("Fail", "Review", "Pass")}
        options = ["All", "Fail", "Review", "Pass"]
        shown = show_col.segmented_control(
            "Show",
            options,
            default="All",
            format_func=lambda s: f"{s} {counts[s] if s in counts else len(chosen.results)}",
        )
        html(f'<p class="sc-facts">{product_facts(by_name.get(picked, {}))}</p>')
        html(compliance_table(chosen, shown or "All"))
        st.download_button(
            "Download compliance list (PDF)",
            to_pdf(chosen, getattr(review, "document_name", None)),
            file_name=f"{chosen.product_id}-compliance.pdf",
            mime="application/pdf",
        )

    with st.container(key="band-compare"):
        html('<span class="sc-anchor" id="sec-compare"></span>')
        label("Compare")
        html(section_head("compare", "Compare products", 2) +
             '<p class="sc-desc">All products of this type, best fit first.</p>')
        html(compare_table(review))

    with st.container(key="band-products"):
        html('<span class="sc-anchor" id="sec-cost"></span>')
        label("Costs")
        html(section_head("cost", "Material cost", 3))
        html(materials_table(review.ranked[0].product_id))
        price_charts()

    with st.container(key="band-spec"):
        html('<span class="sc-anchor" id="sec-spec"></span>')
        label("Source")
        html(section_head("spec", "Original spec", 4))
        with st.expander("View original spec"):
            html(doc_html(spec_text))

    questions = make_questions(review)

    def listing(key: str) -> str:
        return "".join(f"<li>{escape(q)}</li>" for q in questions[key])

    with st.container(key="band-questions"):
        html('<span class="sc-anchor" id="sec-questions"></span>')
        label("Next steps")
        html(section_head("questions", "Questions to ask", 5) +
             '<div class="sc-qcols">'
             f'<div><h3>For the customer</h3><h4>Always ask</h4><ol>{listing("customer_fixed")}</ol>'
             f'<h4>For this spec</h4><ol class="sc-qspec">{listing("customer")}</ol></div>'
             f'<div><h3>For your engineers</h3><h4>Always ask</h4><ol>{listing("engineer_fixed")}</ol>'
             f'<h4>For this spec</h4><ol class="sc-qspec">{listing("engineer")}</ol></div></div>')


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

ABOUT = """
<div class="sc-h2">What this tool does</div>
<div class="sc-about"><p>A customer sends a spec that lists what they need. SpecCheck reads it and checks each item
against your products, so you see fast which product fits and what is missing.</p>
<ol class="sc-steps"><li>Add the customer's spec PDF.</li>
<li>Claude finds each requirement and copies the exact words from the spec.</li>
<li>Simple rules compare each one to your catalog: pass, fail, or review.</li>
<li>You get the best product, the gaps, and questions for the customer.</li></ol></div>
"""


def equipment_panel() -> dict[str, str]:
    with st.container(key="band-about"):
        html(ABOUT)
    return {spec: file for _, specs in EQUIPMENT.values() for spec, file in specs.items()}


def load_example(name: str) -> None:
    st.session_state["example"] = name
    try:
        st.session_state["pasted-spec"] = read_pdfs([(download_file(name).name, file_bytes(download_file(name)))])
    except SpecFileError:
        st.session_state["pasted-spec"] = ""

def example_picker() -> str | None:
    """Example spec PDFs based on real public specs, with the template blanks filled in."""
    files = [e for e in EXAMPLE_FILES if (EXAMPLES / f"{e[0]}.pdf").exists()]
    if not files:
        return None
    picked = st.session_state.get("example")
    html(EXAMPLE_CSS)
    html('<p class="sc-ex-head"><b>Try an example.</b> Real public specs, exactly as published. '
         "Click one to load it, or use the arrow to download it.</p>")
    cols = st.columns(len(files))
    short = {"Veterans Affairs": "VA", "Northwestern Univ.": "NU", "Washington State Univ.": "WSU"}
    for col, (name, kind, kind_label, rating, section, org) in zip(cols, files):
        with col, st.container(key=f"exc-{kind}-{name}"):
            on = " on" if picked == name else ""
            html(f'<div class="sc-ex{on}"><span class="l1"><b>{escape(rating)}</b><span>{kind_label}</span></span>'
                 f'<span class="o"><b>{short.get(org, "")}</b>{escape(org)}</span><span class="s">Sec {section}</span></div>')
            st.button("Load this example", key=f"try-{name}", on_click=load_example, args=(name,))
            st.download_button(":material/download:", file_bytes(download_file(name)), file_name=download_file(name).name,
                               mime="application/pdf", key=f"pdf-{name}", help="Download the original PDF")
    return picked if any(picked == e[0] for e in files) else None


def claude_panel() -> None:
    html('<span class="sc-anchor" id="sec-live"></span>')
    html(f'<div class="sc-h2" style="margin-top:28px">{icon("live", "#1f5f9e")}Check your own spec</div>')
    html('<p class="sc-sub">Upload a PDF or paste the text.</p>')
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

    uploads = st.file_uploader(
        "Spec PDFs",
        type="pdf",
        accept_multiple_files=True,
        help="Add the spec and any addenda. Scanned pages without text won't work.",
    )
    if uploads:
        sig = [(u.name, u.size) for u in uploads]
        if st.session_state.get("upload-sig") != sig:
            st.session_state["upload-sig"] = sig
            try:
                st.session_state["pasted-spec"] = read_pdfs([(u.name, u.getvalue()) for u in uploads])
            except SpecFileError as error:
                st.error(str(error))
    with st.container(key="exband"):
        example_picker()
    current = st.session_state.get("pasted-spec", "").strip()
    first = escape(next((ln.strip() for ln in current.splitlines() if ln.strip()), "Nothing loaded yet")[:80])
    html(f'<div class="sc-words" style="text-align:left;margin:0 0 4px"><b>Spec text</b> · {len(current.split()):,} words · {first}</div>')
    with st.expander("Show or hide the spec text", expanded=False):
        pasted = st.text_area("Spec text", height=220, key="pasted-spec", label_visibility="collapsed",
                              placeholder="Paste the spec text here, or upload a PDF or click an example above.").strip()
    if pasted and st.button("Run review", type="primary"):
        if not review_counter().take(daily_limit()):
            st.warning("Today's review limit has been reached. Please try again tomorrow.")
            return
        try:
            spec_text = pasted
            with st.spinner("Running..."):
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

SAMPLE_GROUP = {spec: group for group, (_, specs) in EQUIPMENT.items() for spec in specs}


def sample_label(name: str) -> str:
    return f"{EQUIPMENT[SAMPLE_GROUP[name]][0]} {name}"


def show_samples() -> None:
    st.session_state["showing"] = "sample"


with st.container(key="band-demo"):
    html('<span class="sc-anchor" id="sec-samples"></span>')
    label("Demo")
    html(f'<div class="sc-h2">Try a sample spec</div>')
    names = list(sample_names)
    name = st.segmented_control(
        "Sample spec",
        names,
        default=names[0],
        format_func=sample_label,
        key="sample",
        on_change=show_samples,
        label_visibility="collapsed",
    ) or names[0]
    sample = sample_names[name]
    if name == "Switchgear":
        voltage = st.segmented_control("Voltage", list(SWITCHGEAR), default=list(SWITCHGEAR)[0],
                                       key="switchgear-voltage", on_change=show_samples) or list(SWITCHGEAR)[0]
        sample = SWITCHGEAR[voltage]
    if name == "Real specs":
        real = st.segmented_control("Real spec", list(REAL_SPECS), default=list(REAL_SPECS)[0],
                                    key="real-spec", on_change=show_samples) or list(REAL_SPECS)[0]
        sample = REAL_SPECS[real]
        st.caption("Based on real public specs from the VA and two universities. The originals are templates "
                   "with blanks, so these copies fill in the values. For testing only.")
    sample_review, sample_text = saved_review(sample)
    type_box(sample_review.equipment_type)
    st.download_button(
        "Download the original PDF" if sample in ORIGINAL_FILES else "Download this sample PDF",
        file_bytes(download_file(sample)),
        file_name=download_file(sample).name,
        mime="application/pdf",
    )
    st.caption("These examples are mainly for these products only: MV switchgear, LV switchgear and UPS.")
    claude_panel()

if st.session_state.get("showing") == "claude" and "review" in st.session_state:
    show_review(st.session_state["review"], st.session_state["review_text"])
else:
    show_review(sample_review, sample_text, show_type=False)

html(JUMP)
html(RAIL)
components.html(REVEAL_JS, height=0)
