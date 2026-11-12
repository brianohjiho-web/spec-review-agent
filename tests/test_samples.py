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
NAMES = ["red_oak_mv", "harbor_lv", "high_desert_mv", "ridgeline_cable_bus", "lakeshore_iso_bus", "prairie_non_seg",
         "mill_creek_utility", "summit_transformer", "orion_ups", "atlas_server_racks"]


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


def test_each_bus_type_only_checks_its_own_products():
    text, spec, _ = load("lakeshore_iso_bus")
    ids = [c.product_id for c in build_review(spec, load_catalog(), text).ranked]
    assert all(i.startswith("IPB") for i in ids) and len(ids) == 4


def test_momentary_rating_rules_out_smaller_cable_bus():
    text, spec, _ = load("ridgeline_cable_bus")
    ranked = build_review(spec, load_catalog(), text).ranked
    small = next(c for c in ranked if c.product_id == "CBL-15-2000")
    failed = [r.requirement.parameter for r in small.results if r.status == "FAIL"]
    assert "momentary_ka" in failed and "bus_current_a" in failed


def test_mva_and_lb_units_convert():
    text, spec, _ = load("summit_transformer")
    ranked = build_review(spec, load_catalog(), text).ranked
    smaller = next(c for c in ranked if c.product_id == "XFM-38-20000")
    assert "power_kva" in [r.requirement.parameter for r in smaller.results if r.status == "FAIL"]
    text, spec, _ = load("atlas_server_racks")
    best = build_review(spec, load_catalog(), text).ranked[0]
    weight = next(r for r in best.results if r.requirement.parameter == "static_load_kg")
    assert weight.status == "PASS"


def test_budget_and_price():
    text, spec, _ = load("orion_ups")
    ranked = build_review(spec, load_catalog(), text).ranked
    assert ranked[0].price_usd == 650000
    budget = next(r for r in ranked[0].results if r.requirement.parameter == "price_usd")
    assert budget.status == "PASS"
    spec.requirements[-1].value_number = 600000
    over = build_review(spec, load_catalog(), None).ranked
    best = next(c for c in over if c.product_id == "UPS-480-1500")
    assert "price_usd" in [r.requirement.parameter for r in best.results if r.status == "FAIL"]


def test_price_breaks_ties():
    from speccheck.checks import rank_products
    from speccheck.models import ProductCheck

    cheap = ProductCheck(product_id="a", product_name="a", price_usd=10, results=[])
    pricey = ProductCheck(product_id="b", product_name="b", price_usd=20, results=[])
    assert rank_products([pricey, cheap]) == [cheap, pricey]
