"""SpecCheck AI web app. Run it with: streamlit run app.py"""
import json
import os
from pathlib import Path

import pandas as pd
import streamlit as st
from anthropic import APIError
from dotenv import load_dotenv

from speccheck.agent import AgentError, SpecAgent
from speccheck.catalog import load_catalog
from speccheck.checks import RULES
from speccheck.models import ProductCheck, Review, SpecRequirements
from speccheck.pdf import SpecFileError, read_pdf
from speccheck.review import build_review, to_csv

ROOT = Path(__file__).parent
SAMPLES = ROOT / "data" / "samples"
SAMPLE_NAMES = {
    "Project Red Oak: 13.8 kV data center": "red_oak_mv",
    "Harbor Colo: 480 V service": "harbor_lv",
    "High Desert: 34.5 kV outdoor": "high_desert_mv",
}
STATUS_LABELS = {"PASS": "Pass", "FAIL": "Fail", "REVIEW": "Review"}
STATUS_COLORS = {"Pass": "#d9f0e1", "Fail": "#f8d9d6", "Review": "#fbecc8"}

load_dotenv(ROOT / ".env")
st.set_page_config(page_title="SpecCheck AI", layout="wide")


@st.cache_data
def catalog() -> list[dict]:
    return load_catalog()


def saved_review(sample: str) -> Review:
    spec_text = read_pdf((SAMPLES / f"{sample}.pdf").read_bytes())
    data = json.loads((SAMPLES / f"{sample}.requirements.json").read_text(encoding="utf-8"))
    return build_review(SpecRequirements(**data), catalog(), spec_text)


def rows(check: ProductCheck) -> pd.DataFrame:
    table = []
    for r in check.results:
        rule = RULES.get(r.requirement.parameter)
        table.append({
            "Status": STATUS_LABELS[r.status],
            "Section": r.requirement.section,
            "Item": rule.label if rule else "Other",
            "Must have": "Yes" if r.requirement.mandatory else "Preferred",
            "Required": r.required,
            "Product": r.product_value,
            "Spec quote": r.requirement.source_quote,
            "Note": r.note,
        })
    return pd.DataFrame(table)


def show_review(review: Review) -> None:
    best = review.ranked[0]
    st.divider()
    if review.recommended_id:
        st.subheader(f"Best match: {best.product_name}")
    else:
        st.subheader("No product meets every must-have item")
        st.write(f"Closest option: **{best.product_name}**")

    columns = st.columns(3)
    columns[0].metric("Must-have items failed", best.mandatory_fails)
    columns[1].metric("Preferred items missed", best.preferred_misses)
    columns[2].metric("Items for engineer review", best.reviews)

    if review.summary:
        st.write(review.summary)
    for question in review.customer_questions:
        st.markdown(f"- {question}")
    if review.source == "saved_example":
        st.caption("Demo mode: these requirements were labeled by hand. Claude was not used.")

    st.subheader("Compliance table")
    names = {c.product_name: c for c in review.ranked}
    chosen = names[st.selectbox("Product", list(names))]
    table = rows(chosen)
    st.dataframe(
        table.style.apply(
            lambda column: [f"background-color: {STATUS_COLORS[v]}; color: #1f2937" for v in column],
            subset=["Status"],
        ),
        hide_index=True,
        width="stretch",
    )
    st.download_button(
        "Download CSV",
        to_csv(chosen),
        file_name=f"{chosen.product_id}-compliance.csv",
        mime="text/csv",
    )

    st.subheader("All products")
    st.dataframe(
        pd.DataFrame([
            {"Product": c.product_name, "Must-have failed": c.mandatory_fails,
             "Preferred missed": c.preferred_misses, "Engineer review": c.reviews}
            for c in review.ranked
        ]),
        hide_index=True,
        width="stretch",
    )
    st.caption("This is a first pass. An engineer must check the results before anything goes to a customer.")


st.title("SpecCheck AI")
st.write("Reads an equipment spec, checks each requirement against a product catalog, and flags what needs a person.")
st.info("All specs and products here are made up for this demo.")

mode = st.radio("Mode", ["Demo with sample specs", "Review my own PDF with Claude"], horizontal=True)

if mode == "Demo with sample specs":
    label = st.selectbox("Sample spec", list(SAMPLE_NAMES))
    sample = SAMPLE_NAMES[label]
    st.download_button("Download this sample PDF", (SAMPLES / f"{sample}.pdf").read_bytes(),
                       file_name=f"{sample}.pdf", mime="application/pdf")
    show_review(saved_review(sample))
else:
    if not os.getenv("ANTHROPIC_API_KEY"):
        st.warning("Add your ANTHROPIC_API_KEY to the .env file, then restart the app.")
    else:
        upload = st.file_uploader("Spec PDF", type="pdf")
        st.caption("The PDF text is sent to the Claude API. Do not upload confidential documents.")
        if upload and st.button("Review spec", type="primary"):
            try:
                spec_text = read_pdf(upload.getvalue())
                with st.spinner("Claude is reviewing the spec..."):
                    st.session_state["review"] = SpecAgent(catalog()).run(spec_text)
            except (SpecFileError, AgentError) as error:
                st.error(str(error))
            except APIError as error:
                st.error(f"The Claude API returned an error: {error}")
        if "review" in st.session_state:
            show_review(st.session_state["review"])
