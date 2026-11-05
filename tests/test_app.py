"""Runs the Streamlit page without a browser."""
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).parent.parent / "app.py")


def page_text(app) -> str:
    return " ".join(m.value for m in app.markdown)


def start(monkeypatch, key=None):
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
    app.button_group[1].set_value("High Desert: 34.5 kV outdoor").run()
    assert not app.exception
    assert "No product meets every must-have item" in page_text(app)


def test_bus_sample(monkeypatch):
    app = start(monkeypatch)
    app.button_group[1].set_value("Lakeshore: iso phase bus").run()
    assert not app.exception
    assert "IPB 15.5 kV Iso Phase Bus, 12000 A" in page_text(app)


def test_equipment_click_filters_samples(monkeypatch):
    app = start(monkeypatch)
    app.button(key="equipment-UPS").click().run()
    assert not app.exception
    assert "UPS 1.5 MW, 480 V" in page_text(app)
    app.button(key="equipment-UPS").click().run()
    assert "UTL 15 kV Service Section, 1200 A" in page_text(app)


def test_status_filter(monkeypatch):
    app = start(monkeypatch)
    app.button(key="equipment-Switchgear").click().run()
    app.button_group[2].set_value("Review").run()
    assert not app.exception
    assert "Needs engineer review" in page_text(app) and "15 kV min" not in page_text(app)


def test_live_mode_asks_for_a_key(monkeypatch):
    app = start(monkeypatch)
    app.button_group[0].set_value("Check your own spec").run()
    assert not app.exception
    assert "ANTHROPIC_API_KEY" in app.warning[0].value


def test_placeholder_key_counts_as_missing(monkeypatch):
    app = start(monkeypatch, key="your_key_here")
    app.button_group[0].set_value("Check your own spec").run()
    assert "ANTHROPIC_API_KEY" in app.warning[0].value


def test_password_gate(monkeypatch):
    app = start(monkeypatch, key="test-key")
    monkeypatch.setenv("APP_PASSWORD", "secret")
    app.button_group[0].set_value("Check your own spec").run()
    assert len(app.text_input) == 1 and not app.warning
    app.text_input[0].set_value("wrong").run()
    assert "Enter the demo password" in app.info[0].value
    app.text_input[0].set_value("secret").run()
    assert not app.info
