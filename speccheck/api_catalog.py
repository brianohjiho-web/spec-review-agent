"""Loads products from a company's product API instead of the JSON file.

Off by default. Turn it on by setting PRODUCT_API_URL (in .env or Streamlit Secrets).
Each company's API names its fields differently, so edit FIELD_MAP and TYPE_MAP below
to match theirs. Everything else in SpecCheck stays the same.

Settings:
  PRODUCT_API_URL   The address that returns the product list, e.g. https://api.example.com/v1/products
  PRODUCT_API_KEY   Their key, if they gave you one. Never put it in GitHub.
  PRODUCT_API_AUTH  How the key is sent: "bearer" (default) or a header name such as "X-API-Key".
"""
import json
import os
import urllib.request
from urllib.parse import urljoin, urlsplit

# Their field name -> SpecCheck field name. Change the left side to match their API.
FIELD_MAP = {
    "sku": "id",
    "name": "name",
    "manufacturer": "maker",
    "category": "equipment_type",
    "max_voltage_kv": "voltage_kv",
    "bil_kv": "bil_kv",
    "continuous_current_a": "bus_current_a",
    "short_circuit_ka": "short_circuit_ka",
    "momentary_ka": "momentary_ka",
    "frequency_hz": "frequency_hz",
    "kva": "power_kva",
    "kw": "power_kw",
    "efficiency_pct": "efficiency_pct",
    "phases": "phases",
    "enclosure": "enclosure",
    "arc_rating": "arc_resistance",
    "location": "location",
    "standards": "standards",
    "features": "features",
    "height_in": "height_in",
    "width_in": "width_in",
    "depth_in": "depth_in",
    "lead_time_weeks": "lead_time_weeks",
    "list_price_usd": "price_usd",
    "url": "source_url",
}

# Their category name -> SpecCheck equipment type. Products in other categories are skipped.
TYPE_MAP = {
    "medium voltage switchgear": "mv_switchgear",
    "low voltage switchgear": "lv_switchgear",
    "load interrupter switchgear": "utility_service",
    "pad-mounted transformer": "transformer",
    "cable bus": "cable_bus",
    "non-segregated phase bus": "non_seg_bus",
    "isolated phase bus": "iso_phase_bus",
    "ups": "ups",
    "server rack": "server_rack",
}

# SpecCheck fields that hold a list of options, not one value.
LIST_FIELDS = {"frequency_hz", "phases", "enclosure", "arc_resistance", "location", "standards", "features",
               "breaker_type", "bus_material", "insulation", "enclosure_material", "cooling",
               "insulating_fluid", "battery_type", "cable_entry", "rack_width_mm"}


def enabled() -> bool:
    return bool(os.getenv("PRODUCT_API_URL"))


def _get(url: str, key: str | None, auth: str, timeout: int) -> dict | list:
    headers = {"Accept": "application/json"}
    if key:
        if auth.lower() == "bearer":
            headers["Authorization"] = f"Bearer {key}"
        else:
            headers[auth] = key
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_items(url: str, key: str | None = None, auth: str = "bearer", timeout: int = 30, max_pages: int = 200) -> list[dict]:
    """Gets every product, following a "next" link if the API pages its results."""
    items, pages = [], 0
    origin = urlsplit(url)
    while url and pages < max_pages:
        data = _get(url, key, auth, timeout)
        if isinstance(data, list):
            items.extend(data)
            break
        items.extend(data.get("products") or data.get("items") or data.get("data") or [])
        nxt = data.get("next") or (data.get("links") or {}).get("next")
        if nxt:
            next_url = urljoin(url, nxt)
            next_origin = urlsplit(next_url)
            if (next_origin.scheme, next_origin.netloc) != (origin.scheme, origin.netloc):
                raise ValueError("Product API pagination link changed origin; refusing to send credentials.")
            url = next_url
        else:
            url = None
        pages += 1
    return items


def to_product(item: dict) -> dict | None:
    """Turns one API record into a SpecCheck product, or None if it isn't a type we check."""
    p = {}
    for theirs, ours in FIELD_MAP.items():
        value = item.get(theirs)
        if value in (None, ""):
            continue
        if ours in LIST_FIELDS and not isinstance(value, list):
            value = [v.strip() for v in str(value).split(",")] if isinstance(value, str) else [value]
        p[ours] = value
    kind = str(p.get("equipment_type", "")).strip().lower()
    p["equipment_type"] = TYPE_MAP.get(kind, kind if kind in TYPE_MAP.values() else "")
    if not p.get("id") or not p.get("name") or not p["equipment_type"]:
        return None
    p.setdefault("maker", "")
    # Company data is the full option list, so an option it doesn't list is a real "no".
    p["lists_complete"] = True
    p["source_note"] = "From the company product API."
    return p


def load_from_api() -> list[dict]:
    items = fetch_items(os.environ["PRODUCT_API_URL"], os.getenv("PRODUCT_API_KEY"),
                        os.getenv("PRODUCT_API_AUTH", "bearer"))
    products = [p for p in map(to_product, items) if p]
    if not products:
        raise ValueError("The product API returned no products SpecCheck can use. Check FIELD_MAP and TYPE_MAP.")
    return products
