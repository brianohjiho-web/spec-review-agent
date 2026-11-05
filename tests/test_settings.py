from datetime import date

from speccheck.settings import DailyCounter, has_api_key, password_ok


def test_key_check(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert not has_api_key()
    monkeypatch.setenv("ANTHROPIC_API_KEY", "your_key_here")
    assert not has_api_key()
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    assert has_api_key()


def test_password(monkeypatch):
    monkeypatch.delenv("APP_PASSWORD", raising=False)
    assert password_ok("anything")
    monkeypatch.setenv("APP_PASSWORD", "secret")
    assert password_ok("secret") and not password_ok("nope")


def test_daily_limit_and_reset():
    counter = DailyCounter()
    day = date(2026, 11, 2)
    assert counter.take(2, day) and counter.take(2, day) and not counter.take(2, day)
    assert counter.take(2, date(2026, 11, 3))
    assert all(DailyCounter().take(0, day) for _ in range(3))
