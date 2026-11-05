"""App settings from the .env file, plus optional public demo limits."""
import hmac
import os
from datetime import date
from threading import Lock

PLACEHOLDER = "your_key_here"


def has_api_key() -> bool:
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    return bool(key) and key != PLACEHOLDER


def app_password() -> str:
    return os.getenv("APP_PASSWORD", "").strip()


def password_ok(entered: str) -> bool:
    """Returns True when no password is set, or when the entry matches."""
    expected = app_password()
    return not expected or hmac.compare_digest(entered.encode(), expected.encode())


def daily_limit() -> int:
    """The most Claude reviews allowed per day. 0 means no limit."""
    try:
        return max(0, int(os.getenv("DAILY_REVIEW_LIMIT", "0")))
    except ValueError:
        return 0


class DailyCounter:
    """Counts Claude reviews for the current day."""

    def __init__(self):
        self.lock = Lock()
        self.day = date.today()
        self.count = 0

    def take(self, limit: int, today: date | None = None) -> bool:
        """Uses one review. Returns False if today's limit is already reached."""
        today = today or date.today()
        with self.lock:
            if today != self.day:
                self.day, self.count = today, 0
            if limit and self.count >= limit:
                return False
            self.count += 1
            return True
