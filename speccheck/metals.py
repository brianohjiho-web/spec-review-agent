"""Material prices for the cost estimate.

Copper, aluminum, lead, nickel, and Brent oil prices come from FRED (Federal Reserve Bank
of St. Louis), which publishes the IMF's monthly global prices. No API key is
needed. If the download fails, the saved prices in data/metal_prices.json are
used. Steel, electrical steel, lithium, and transformer oil have no free dollar
price, so the user enters those prices. FRED price indexes show their trends.
"""
import csv
import json
import urllib.request
from io import StringIO
from pathlib import Path

SNAPSHOT = Path(__file__).parent.parent / "data" / "metal_prices.json"
URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
LB_PER_METRIC_TON = 2204.62
MONTHS = 13

LIVE = {"copper": "Copper", "aluminum": "Aluminum", "lead": "Lead", "nickel": "Nickel"}
ENTERED = {
    "steel": ("Steel", "lb"),
    "electrical_steel": ("Electrical steel", "lb"),
    "lithium": ("Lithium", "lb"),
    "transformer_oil": ("Transformer oil", "gal"),
}
# key: (name, kind, note). Kind is "ton" ($ per metric ton), "barrel", or "index".
CHARTS = {
    "copper": ("Copper", "ton", ""),
    "aluminum": ("Aluminum", "ton", ""),
    "lead": ("Lead", "ton", ""),
    "nickel": ("Nickel", "ton", ""),
    "steel": ("Steel", "index", "Price index for steel mill products"),
    "electrical_steel": ("Electrical steel", "index", "Closest index: cold-rolled steel sheet"),
    "transformer_oil": ("Transformer oil", "index", "Closest index: lubricating oils"),
    "brent": ("Brent crude oil", "barrel", "Oil price trend"),
}


def history_from_csv(text: str, months: int = MONTHS) -> list[list]:
    """Returns the newest months from a FRED CSV download as [date, value] pairs."""
    rows = []
    for row in list(csv.reader(StringIO(text)))[1:]:
        if len(row) != 2:
            continue
        try:
            rows.append([row[0], float(row[1])])
        except ValueError:  # FRED marks missing months with "."
            continue
    if not rows:
        raise ValueError("No prices found.")
    return rows[-months:]


def saved_prices() -> dict:
    data = json.loads(SNAPSHOT.read_text(encoding="utf-8"))["series"]
    return {name: {**series, "live": False} for name, series in data.items()}


def latest_prices(timeout: float = 8) -> dict:
    """Tries FRED for each series and falls back to the saved prices."""
    prices = saved_prices()
    for name, series in prices.items():
        try:
            with urllib.request.urlopen(URL.format(series["id"]), timeout=timeout) as response:
                series["history"] = history_from_csv(response.read().decode("utf-8"))
            series["live"] = True
        except Exception:
            pass
    return prices


def per_lb(series: dict) -> float:
    return series["history"][-1][1] / LB_PER_METRIC_TON


def material_cost(materials: dict, prices: dict, entered: dict | None = None) -> list[dict]:
    """One row per material in the product. Entered prices are per lb or per gallon."""
    entered = entered or {}
    rows = []
    for key, amount in (materials or {}).items():
        if not amount:
            continue
        if key in LIVE:
            own = entered.get(key)
            price = own or per_lb(prices[key])
            rows.append({"key": key, "name": LIVE[key], "amount": amount, "unit": "lb", "price": price,
                         "cost": amount * price, "source": "entered" if own else "FRED"})
        elif key in ENTERED:
            name, unit = ENTERED[key]
            price = entered.get(key) or None
            rows.append({"key": key, "name": name, "amount": amount, "unit": unit, "price": price,
                         "cost": amount * price if price else None, "source": "entered"})
    return rows
