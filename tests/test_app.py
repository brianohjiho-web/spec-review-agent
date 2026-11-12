"""Runs the Streamlit page without a browser."""
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).parent.parent / "app.py")


def page_text(app) -> str:
    return " ".join(m.value for m in app.markdown)


def start(monkeypatch, key=None):
    from speccheck import metals
    monkeypatch.setattr(metals.urllib.request, "urlopen", lambda *a, **k: (_ for _ in ()).throw(OSError("offline")))
    monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **k: False)
    monkeypatch.delenv("APP_PASSWORD", raising=False)
    monkeypatch.delenv("DAILY_REVIEW_LIMIT", raising=False)
    if key:
        monkeypatch.setenv("ANTHROPIC_API_KEY", key)
    else:
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    return AppTest.from_file(APP, default_timeout=30).run()


def test_demo_loads_without_api_key(monkeypatch):
    app = start(monkeypatch)
    assert not app.exception
    text = page_text(app)
    assert "By Brian Oh" in text and "Best match" in text and "15 kV min" in text


def test_sample_with_no_compliant_product(monkeypatch):
    app = start(monkeypatch)
    app.button_group[0].set_value("Outdoor switchgear, 34.5 kV").run()
    assert not app.exception
    assert "No product meets every must-have item" in page_text(app)


def test_bus_sample(monkeypatch):
    app = start(monkeypatch)
    app.button_group[0].set_value("Iso phase bus").run()
    assert not app.exception
    assert "IPB 15.5 kV Iso Phase Bus, 12000 A" in page_text(app)
    assert "own metal tube" in page_text(app)


def test_equipment_click_filters_samples(monkeypatch):
    app = start(monkeypatch)
    app.button(key="equipment-UPS").click().run()
    assert not app.exception
    assert "UPS 1.5 MW, 480 V" in page_text(app) and "Product comparison" not in page_text(app)
    assert "$700,000 max" in page_text(app)
    assert "Material cost estimate" in page_text(app) and "Lithium ($/lb)" in str(app.number_input)
    assert "Price trends" in page_text(app) and "cold-rolled steel sheet" in page_text(app)
    assert "Battery backup" in page_text(app)
    app.button(key="equipment-UPS").click().run()
    assert "UTL 15 kV Service Section, 1200 A" in page_text(app)


def test_status_filter(monkeypatch):
    app = start(monkeypatch)
    app.button(key="equipment-Switchgear").click().run()
    app.button_group[1].set_value("Review").run()
    assert not app.exception
    assert "Needs engineer review" in page_text(app) and "15 kV min" not in page_text(app)


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


def test_entered_steel_price_adds_cost(monkeypatch):
    app = start(monkeypatch)
    app.button(key="equipment-Switchgear").click().run()
    before = page_text(app)
    app.number_input(key="price-steel").set_value(0.5).run()
    assert not app.exception and "Steel</span>" in page_text(app) and "Steel</span>" not in before


def test_calculator_has_every_chart_metal(monkeypatch):
    app = start(monkeypatch)
    keys = {n.key for n in app.number_input}
    assert {"price-copper", "price-aluminum", "price-lead", "price-nickel", "price-steel"} <= keys


def test_spec_shows_as_document(monkeypatch):
    app = start(monkeypatch)
    text = page_text(app)
    assert '<article class="sc-docpage"><h1>Mill Creek Data Center: Utility Service Section</h1>' in text
    assert "<h2>2. Ratings</h2>" in text


def test_price_split_adds_to_100(monkeypatch):
    app = start(monkeypatch)
    text = page_text(app)
    assert "= 100%" in text and "Other costs (labor, parts, overhead)" in text
