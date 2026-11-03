"""Loads the sample product catalog."""
import json
from pathlib import Path

DEFAULT_CATALOG = Path(__file__).parent.parent / "data" / "catalog.json"


def load_catalog(path: Path = DEFAULT_CATALOG) -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))["products"]


def by_type(catalog: list[dict], equipment_type: str) -> list[dict]:
    return [p for p in catalog if p["equipment_type"] == equipment_type]


def find_product(catalog: list[dict], product_id: str) -> dict | None:
    return next((p for p in catalog if p["id"] == product_id), None)
