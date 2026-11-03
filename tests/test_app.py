"""Runs the Streamlit page without a browser."""
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).parent.parent / "app.py")


def test_demo_loads_without_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    app = AppTest.from_file(APP, default_timeout=30).run()
    assert not app.exception
    assert "No product meets" in app.subheader[0].value


def test_sample_with_no_compliant_product(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    app = AppTest.from_file(APP, default_timeout=30).run()
    app.selectbox[0].select("High Desert: 34.5 kV outdoor").run()
    assert not app.exception
    assert "No product meets" in app.subheader[0].value


def test_live_mode_asks_for_a_key(monkeypatch):
    monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **k: False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    app = AppTest.from_file(APP, default_timeout=30).run()
    app.radio[0].set_value("Review my own PDF with Claude").run()
    assert not app.exception
    assert "ANTHROPIC_API_KEY" in app.warning[0].value
