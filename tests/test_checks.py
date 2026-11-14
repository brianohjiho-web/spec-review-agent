import pytest

from speccheck.checks import check_requirement, rank_products, to_catalog_unit, verify_source
from speccheck.models import ProductCheck, Requirement
from speccheck.review import _safe_cell, to_csv

PRODUCT = {"id": "P1", "name": "Test", "voltage_kv": 15.0, "bus_current_a": 3000, "lead_time_weeks": 52,
           "max_altitude_m": 1000, "max_ambient_c": 40, "control_voltage_vdc": [125, 250],
           "arc_resistance": [], "features": ["remote racking"], "bil_kv": None}


def req(parameter, number=None, unit="", text=None, mandatory=True, quote=""):
    return Requirement(id="R1", parameter=parameter, value_number=number, unit=unit, value_text=text,
                       mandatory=mandatory, source_quote=quote)


@pytest.mark.parametrize("requirement, status", [
    (req("voltage_kv", 15, "kV"), "PASS"),      # Exactly at the limit
    (req("voltage_kv", 15.1, "kV"), "FAIL"),
    (req("voltage_kv", 480, "V"), "PASS"),      # Volts convert to kV
    (req("bus_current_a", 3, "kA"), "PASS"),    # kA converts to A
    (req("bus_current_a", 4000, "A"), "FAIL"),
    (req("lead_time_weeks", 52, "weeks"), "PASS"),
    (req("lead_time_weeks", 40, "weeks"), "FAIL"),  # Lower is better here
    (req("max_altitude_m", 6500, "ft"), "FAIL"),    # 6,500 ft is about 1,981 m
    (req("max_ambient_c", 113, "F"), "FAIL"),       # 113 F is 45 C
    (req("control_voltage_vdc", 250, "VDC"), "PASS"),
    (req("control_voltage_vdc", 48, "VDC"), "FAIL"),
    (req("features", text="Remote Racking"), "PASS"),
    (req("features", text="infrared windows"), "FAIL"),
    (req("arc_resistance", text="Type 2B"), "FAIL"),   # An empty list means none
    (req("features", text="gold-plated doors"), "REVIEW"),  # Not a known value
    (req("voltage_kv", 15, "furlongs"), "REVIEW"),     # Unknown unit
    (req("voltage_kv", 15), "REVIEW"),                 # Missing unit
    (req("voltage_kv"), "REVIEW"),                     # Missing value
    (req("bil_kv", 95, "kV"), "REVIEW"),               # Catalog value is unknown
    (req("other", text="Witness testing"), "REVIEW"),
])
def test_statuses(requirement, status):
    assert check_requirement(requirement, PRODUCT).status == status


def test_unit_conversion():
    assert to_catalog_unit("max_altitude_m", 1000, "ft") == pytest.approx(304.8)
    assert to_catalog_unit("max_ambient_c", 104, "°F") == pytest.approx(40)


SPEC = "The main bus\nshall be rated 3,000 A continuous."


@pytest.mark.parametrize("quote, value, ok", [
    ("main bus shall be rated 3,000 A", 3000, True),     # Handles PDF line breaks
    ("rated 4,000 A continuous", 4000, False),           # Made-up quote
    ("main bus shall be rated 3,000 A", 4000, False),    # Real quote, wrong value
    ("", 3000, False),
])
def test_source_check(quote, value, ok):
    requirement = req("bus_current_a", value, "A", quote=quote)
    assert (verify_source(requirement, SPEC) is None) is ok


def test_bad_source_overrides_a_pass():
    requirement = req("bus_current_a", 1000, "A", quote="this text is not in the spec 1000")
    result = check_requirement(requirement, PRODUCT, SPEC)
    assert result.status == "REVIEW"


def test_bad_source_overrides_a_fail():
    requirement = req("bus_current_a", 4000, "A", quote="this text is not in the spec 4000")
    assert check_requirement(requirement, PRODUCT, SPEC).status == "REVIEW"


def check_with(*statuses):
    results = [check_requirement(req("bus_current_a", 1, "A"), PRODUCT) for _ in statuses]
    for result, (status, mandatory) in zip(results, statuses):
        result.status = status
        result.requirement.mandatory = mandatory
    return ProductCheck(product_id=str(statuses), product_name="Test", results=results)


def test_ranking_puts_mandatory_fails_last():
    bad = check_with(("FAIL", True))
    preferred = check_with(("FAIL", False))
    review = check_with(("REVIEW", True))
    clean = check_with(("PASS", True))
    assert rank_products([bad, preferred, review, clean]) == [clean, preferred, review, bad]


def test_csv_blocks_formulas():
    assert _safe_cell('=HYPERLINK("x")').startswith("'=")
    requirement = req("other", text="=1+1", quote="=1+1")
    check = ProductCheck(product_id="P", product_name="P", results=[check_requirement(requirement, PRODUCT)])
    assert "'=1+1" in to_csv(check)


def test_phases_and_enclosure_size():
    from speccheck.checks import check_requirement
    from speccheck.models import Requirement
    product = {"phases": [3], "height_in": 90, "width_in": 120, "depth_in": None}

    def status(parameter, number, unit):
        req = Requirement(id="R1", parameter=parameter, value_number=number, value_text=None, unit=unit,
                          mandatory=True, section="1", source_quote="x")
        return check_requirement(req, product).status

    assert status("phases", 3, "") == "PASS" and status("phases", 1, "") == "FAIL"
    assert status("height_in", 7.5, "ft") == "PASS" and status("height_in", 88, "in.") == "FAIL"
    assert status("width_in", 3100, "mm") == "PASS" and status("width_in", 3, "m") == "FAIL"
    assert status("depth_in", 60, "in") == "REVIEW"


def test_public_catalog_has_sources_and_known_fields():
    import json
    from pathlib import Path
    from speccheck.checks import RULES
    data = json.loads((Path(__file__).parent.parent / "data" / "catalog_public.json").read_text())
    types = {p["equipment_type"] for p in data["products"]}
    assert len(types) == 9
    for p in data["products"]:
        assert p["source_url"].startswith("https://") and p["maker"]
        assert "price_usd" in p and p["price_usd"] is None
        for key in RULES:
            assert key in p


def test_public_list_gap_is_review_not_fail():
    from speccheck.checks import check_requirement
    from speccheck.models import Requirement
    req = Requirement(id="R1", parameter="features", value_number=None, value_text="zone selective interlocking",
                      unit="", mandatory=True, section="1", source_quote="x")
    assert check_requirement(req, {"features": ["drawout breakers"]}).status == "FAIL"
    assert check_requirement(req, {"features": ["drawout breakers"], "lists_complete": False}).status == "REVIEW"


def test_number_words_in_quotes():
    from speccheck.checks import verify_source
    from speccheck.models import Requirement
    req = Requirement(id="R1", parameter="phases", value_number=3, value_text=None, unit="", mandatory=True,
                      section="5", source_quote="three-phase")
    assert verify_source(req, "SIMOSEC is a three-phase indoor switchgear.") is None


def test_three_questions_each():
    import json
    from pathlib import Path
    from speccheck.checks import check_product, rank_products
    from speccheck.catalog import load_catalog
    from speccheck.models import Review, SpecRequirements
    from speccheck.questions import make_questions
    samples = Path(__file__).parent.parent / "data" / "samples"
    for path in samples.glob("*.requirements.json"):
        spec = SpecRequirements(**json.loads(path.read_text()))
        ranked = rank_products([check_product(spec.requirements, p) for p in load_catalog()
                                if p["equipment_type"] == spec.equipment_type])
        q = make_questions(Review(equipment_type=spec.equipment_type, ranked=ranked))
        assert all(len(q[k]) == 3 for k in ("customer_fixed", "engineer_fixed", "customer", "engineer")), path.name


def test_missing_product_data_goes_to_engineers():
    import json
    from pathlib import Path
    from speccheck.catalog import PUBLIC_CATALOG, load_catalog
    from speccheck.checks import check_product, rank_products
    from speccheck.models import Review, SpecRequirements
    from speccheck.questions import make_questions
    path = Path(__file__).parent.parent / "data" / "samples" / "mill_creek_utility.requirements.json"
    spec = SpecRequirements(**json.loads(path.read_text()))
    ranked = rank_products([check_product(spec.requirements, p) for p in load_catalog(PUBLIC_CATALOG)
                            if p["equipment_type"] == spec.equipment_type])
    q = make_questions(Review(equipment_type=spec.equipment_type, ranked=ranked))
    assert not any("confirm the exact value" in x for x in q["customer"])
    assert any("our product data doesn't say" in x for x in q["engineer"])


def test_pdf_export_is_a_pdf():
    from speccheck.models import CheckResult, ProductCheck, Requirement
    from speccheck.review import to_pdf
    req = Requirement(id="R1", section="2", parameter="voltage_kv", value=15, unit="kV", source_quote="rated 15 kV <b>", mandatory=True)
    check = ProductCheck(product_id="X", product_name="Test & Co", results=[CheckResult(requirement=req, status="PASS", required="15 kV", product_value="15 kV", note="")])
    data = to_pdf(check, "Spec A")
    assert data[:5] == b"%PDF-" and len(data) > 1000
