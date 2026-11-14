"""Runs the Streamlit page without a browser."""
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).parent.parent / "app.py")


def page_text(app) -> str:
    return " ".join(m.value for m in app.markdown)


def start(monkeypatch, key=None, catalog="Demo catalog with prices"):
    from speccheck import metals
    monkeypatch.setattr(metals.urllib.request, "urlopen", lambda *a, **k: (_ for _ in ()).throw(OSError("offline")))
    monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **k: False)
    monkeypatch.delenv("APP_PASSWORD", raising=False)
    monkeypatch.delenv("DAILY_REVIEW_LIMIT", raising=False)
    if key:
        monkeypatch.setenv("ANTHROPIC_API_KEY", key)
    else:
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    app = AppTest.from_file(APP, default_timeout=30)
    app.session_state["catalog_choice"] = catalog
    return app.run()


def test_demo_loads_without_api_key(monkeypatch):
    app = start(monkeypatch)
    assert not app.exception
    text = page_text(app)
    assert "Brian Oh" in text and "Best match" in text and "kV min" in text


def test_sample_with_no_compliant_product(monkeypatch):
    app = start(monkeypatch)
    app.button_group[0].set_value("Switchgear").run()
    app.button_group[1].set_value("34.5 kV · outdoor").run()
    assert not app.exception
    assert "No product meets every must-have item" in page_text(app)


def test_bus_sample(monkeypatch):
    app = start(monkeypatch)
    app.button_group[0].set_value("Iso phase bus").run()
    assert not app.exception
    assert "IPB 15.5 kV Iso Phase Bus, 12000 A" in page_text(app)
    assert "own metal tube" in page_text(app)


def test_ups_sample(monkeypatch):
    app = start(monkeypatch)
    app.button_group[0].set_value("UPS").run()
    assert not app.exception
    assert "UPS 1.5 MW, 480 V" in page_text(app) and "Product comparison" not in page_text(app)
    assert "$700,000 max" in page_text(app)
    assert "Material cost estimate" in page_text(app)
    assert "Price trends" in page_text(app) and "cold-rolled steel sheet" in page_text(app)
    assert "Battery backup" in page_text(app)
    app.button_group[0].set_value("Utility service").run()
    assert "UTL 15 kV Service Section, 1200 A" in page_text(app)


def test_status_filter(monkeypatch):
    app = start(monkeypatch)
    app.button_group[0].set_value("Switchgear").run()
    app.button_group[1].set_value("13.8 kV · indoor").run()
    app.button_group[2].set_value("Review").run()
    assert not app.exception
    matrix = next(m.value for m in app.markdown if 'class="sc-matrix"' in m.value)
    assert "An engineer should read it" in matrix and "15 kV min" not in matrix


def test_live_mode_asks_for_a_key(monkeypatch):
    app = start(monkeypatch)
    assert not app.exception
    assert "ANTHROPIC_API_KEY" in app.warning[0].value


def test_placeholder_key_counts_as_missing(monkeypatch):
    app = start(monkeypatch, key="your_key_here")
    assert "ANTHROPIC_API_KEY" in app.warning[0].value


def test_password_gate(monkeypatch):
    app = start(monkeypatch, key="test-key")
    monkeypatch.setenv("APP_PASSWORD", "secret")
    app.run()
    assert len(app.text_input) == 1 and not app.warning
    app.text_input[0].set_value("wrong").run()
    assert "Enter the demo password" in app.info[0].value
    app.text_input[0].set_value("secret").run()
    assert not app.info


def test_typed_key_unlocks_upload(monkeypatch):
    app = start(monkeypatch)
    assert len(app.text_input) == 1 and app.warning
    app.text_input[0].set_value("sk-test").run()
    assert not app.exception and not app.warning


def test_streamlit_secret_is_used(monkeypatch):
    monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **k: False)
    for name in ("ANTHROPIC_API_KEY", "APP_PASSWORD", "DAILY_REVIEW_LIMIT"):
        monkeypatch.delenv(name, raising=False)
    app = AppTest.from_file(APP, default_timeout=30)
    app.secrets["ANTHROPIC_API_KEY"] = "sk-test"
    app.run()
    assert not app.exception and not app.text_input and not app.warning
    assert app.get("file_uploader")


def test_samples_and_own_spec_on_one_page(monkeypatch):
    app = start(monkeypatch)
    text = page_text(app)
    assert "Pick a sample spec" in text and "Check your own spec" in text
    assert "confidential" not in text


def test_spec_shows_as_document(monkeypatch):
    app = start(monkeypatch)
    text = page_text(app)
    assert '<article class="sc-docpage"><h1>Mill Creek Data Center: Utility Service Section</h1>' in text
    assert "<h2>2. Ratings</h2>" in text


def test_price_split_adds_to_100(monkeypatch):
    app = start(monkeypatch)
    text = page_text(app)
    assert "= 100%" in text and "Other costs (labor, parts, overhead)" in text


def test_breakdown_lists_every_material(monkeypatch):
    app = start(monkeypatch)
    text = page_text(app)
    for name in ("Copper", "Lead", "Nickel", "Electrical steel", "Lithium", "Transformer oil"):
        assert f"<span>{name}</span>" in text
    assert "Not used" in text


def test_questions_section(monkeypatch):
    app = start(monkeypatch)
    text = page_text(app)
    assert "Questions to ask" in text and "For the customer" in text and "For your engineers" in text
    app.button_group[0].set_value("Switchgear").run()
    app.button_group[1].set_value("34.5 kV · outdoor").run()
    assert "Is this a firm limit, or could ours work?" in page_text(app)


def test_public_catalog(monkeypatch):
    app = start(monkeypatch, catalog="Public datasheets")
    assert not app.exception
    text = page_text(app)
    assert "Siemens SIEBREAK-VCB Metal-Enclosed Switchgear" in text
    assert "source page" in text
    app.button_group[0].set_value("UPS").run()
    assert not app.exception and "UPS" in page_text(app)


def test_public_catalog_is_default(monkeypatch):
    monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **k: False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    app = AppTest.from_file(APP, default_timeout=30).run()
    assert not app.exception and "Siemens SIEBREAK-VCB Metal-Enclosed Switchgear" in page_text(app)


def test_compare_products(monkeypatch):
    app = start(monkeypatch, catalog="Public datasheets")
    text = page_text(app)
    assert "Compare products" in text and 'class="sc-cmp"' in text and "Best match" in text


def test_pdf_material_estimate_uses_default_prices(monkeypatch):
    from speccheck import metals
    monkeypatch.setattr(metals.urllib.request, "urlopen", lambda *a, **k: (_ for _ in ()).throw(OSError("offline")))
    rows = metals.material_cost({"copper": 100, "steel": 1000, "lithium": 5}, metals.saved_prices())
    by_key = {r["key"]: r for r in rows}
    assert by_key["steel"]["cost"] == 650 and by_key["copper"]["cost"] > 0 and by_key["lithium"]["cost"] is None


def test_company_api_catalog_is_used_when_set(monkeypatch):
    from speccheck import api_catalog
    monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **k: False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("PRODUCT_API_URL", "https://api.example.com/v1/products")
    product = {"id": "ACME-15", "name": "Acme Test Switchgear 15 kV", "maker": "Acme", "equipment_type": "utility_service",
               "voltage_kv": 15, "bus_current_a": 1200, "lists_complete": True}
    monkeypatch.setattr(api_catalog, "load_from_api", lambda: [product])
    app = AppTest.from_file(APP, default_timeout=30).run()
    assert not app.exception and "Acme Test Switchgear 15 kV" in page_text(app)
