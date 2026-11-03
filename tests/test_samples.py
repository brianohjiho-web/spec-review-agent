import json
from pathlib import Path

import pytest

from scripts.evaluate import review_matches, score_extraction
from speccheck.catalog import load_catalog
from speccheck.checks import verify_source
from speccheck.models import SpecRequirements
from speccheck.pdf import SpecFileError, read_pdf
from speccheck.review import build_review

SAMPLES = Path(__file__).parent.parent / "data" / "samples"
NAMES = ["red_oak_mv", "harbor_lv", "high_desert_mv"]


def load(name):
    text = read_pdf((SAMPLES / f"{name}.pdf").read_bytes())
    spec = SpecRequirements(**json.loads((SAMPLES / f"{name}.requirements.json").read_text()))
    expected = json.loads((SAMPLES / f"{name}.expected.json").read_text())
    return text, spec, expected


@pytest.mark.parametrize("name", NAMES)
def test_every_label_quote_is_in_the_pdf(name):
    text, spec, _ = load(name)
    assert [verify_source(r, text) for r in spec.requirements] == [None] * len(spec.requirements)


@pytest.mark.parametrize("name", NAMES)
def test_expected_result(name):
    text, spec, expected = load(name)
    assert review_matches(build_review(spec, load_catalog(), text), expected)


def test_lead_time_rules_out_the_oversized_product():
    text, spec, _ = load("red_oak_mv")
    ranked = build_review(spec, load_catalog(), text).ranked
    bigger = next(c for c in ranked if c.product_id == "MVA-15-4000")
    assert [r.requirement.parameter for r in bigger.results if r.status == "FAIL"] == ["lead_time_weeks"]


def test_preferred_miss_does_not_block_a_recommendation():
    text, spec, _ = load("red_oak_mv")
    best = build_review(spec, load_catalog(), text).ranked[0]
    assert best.preferred_misses == 1 and best.mandatory_fails == 0


def test_mandatory_review_blocks_a_recommendation():
    text, spec, _ = load("red_oak_mv")
    spec.requirements[0].source_quote = "This quote is not in the spec."
    review = build_review(spec, load_catalog(), text)
    assert review.ranked[0].results[0].status == "REVIEW"
    assert review.recommended_id is None


def test_empty_requirements_do_not_produce_a_recommendation():
    _, spec, _ = load("red_oak_mv")
    spec.requirements = []
    review = build_review(spec, load_catalog())
    assert review.recommended_id is None


def test_extraction_score_counts_misses_and_extras():
    _, labels, _ = load("harbor_lv")
    found = labels.model_copy(deep=True)
    found.requirements[0].value_number = 999
    score = score_extraction(found, labels)
    assert score["right"] == score["labeled"] - 1
    assert len(score["missed"]) == len(score["extra"]) == 1


def test_bad_pdf_gives_a_clear_error():
    with pytest.raises(SpecFileError):
        read_pdf(b"this is not a pdf")


def test_blank_pdf_gives_a_clear_error():
    from io import BytesIO

    from pypdf import PdfWriter

    writer = PdfWriter()
    writer.add_blank_page(100, 100)
    data = BytesIO()
    writer.write(data)
    with pytest.raises(SpecFileError, match="scan"):
        read_pdf(data.getvalue())
