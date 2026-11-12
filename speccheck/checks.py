"""Plain Python compliance checks. No AI runs in this file.

Claude reads the spec. This code decides pass or fail, so the same inputs
always give the same answer.
"""
import re
from dataclasses import dataclass
from typing import Optional

from .models import CheckResult, ProductCheck, Requirement


@dataclass(frozen=True)
class Rule:
    label: str
    mode: str  # min, max, one_of_number, one_of_text
    unit: str = ""


RULES = {
    "voltage_kv": Rule("Rated maximum voltage", "min", "kV"),
    "bil_kv": Rule("Impulse withstand (BIL)", "min", "kV"),
    "bus_current_a": Rule("Continuous current", "min", "A"),
    "short_circuit_ka": Rule("Short-circuit rating", "min", "kA"),
    "momentary_ka": Rule("Momentary rating", "min", "kA"),
    "frequency_hz": Rule("Frequency", "one_of_number", "Hz"),
    "control_voltage_vdc": Rule("Control voltage", "one_of_number", "VDC"),
    "max_ambient_c": Rule("Ambient temperature", "min", "C"),
    "max_altitude_m": Rule("Site altitude", "min", "m"),
    "lead_time_weeks": Rule("Lead time", "max", "weeks"),
    "price_usd": Rule("Price", "max", "USD"),
    "power_kva": Rule("Power rating", "min", "kVA"),
    "power_kw": Rule("Power rating", "min", "kW"),
    "secondary_voltage_kv": Rule("Secondary voltage", "one_of_number", "kV"),
    "impedance_pct": Rule("Impedance", "one_of_number", "%"),
    "runtime_min": Rule("Battery runtime", "min", "min"),
    "efficiency_pct": Rule("Efficiency", "min", "%"),
    "rack_units": Rule("Rack height", "min", "U"),
    "rack_power_kw": Rule("Rack power", "min", "kW"),
    "static_load_kg": Rule("Static load", "min", "kg"),
    "rack_width_mm": Rule("Rack width", "one_of_number", "mm"),
    "enclosure": Rule("Enclosure", "one_of_text"),
    "arc_resistance": Rule("Arc resistance", "one_of_text"),
    "breaker_type": Rule("Breaker type", "one_of_text"),
    "bus_material": Rule("Conductor material", "one_of_text"),
    "insulation": Rule("Cable insulation", "one_of_text"),
    "enclosure_material": Rule("Enclosure material", "one_of_text"),
    "cooling": Rule("Cooling", "one_of_text"),
    "location": Rule("Location", "one_of_text"),
    "insulating_fluid": Rule("Insulating fluid", "one_of_text"),
    "battery_type": Rule("Battery type", "one_of_text"),
    "cable_entry": Rule("Cable entry", "one_of_text"),
    "standards": Rule("Standard", "one_of_text"),
    "features": Rule("Feature", "one_of_text"),
}

VOCABULARY = {
    "enclosure": ["NEMA 1", "NEMA 3R"],
    "arc_resistance": ["Type 2", "Type 2B"],
    "breaker_type": ["vacuum", "air"],
    "bus_material": ["copper", "tin-plated copper", "silver-plated copper", "aluminum"],
    "insulation": ["EPR", "XLPE"],
    "enclosure_material": ["aluminum", "steel"],
    "cooling": ["self-cooled", "forced-air", "ONAN", "ONAF", "air", "rear-door liquid", "direct-to-chip"],
    "location": ["indoor", "outdoor"],
    "insulating_fluid": ["mineral oil", "natural ester"],
    "battery_type": ["lithium-ion", "VRLA"],
    "cable_entry": ["top", "bottom"],
    "standards": ["IEEE C37.20.1", "IEEE C37.20.2", "IEEE C37.20.7", "IEEE C37.23", "IEEE C37.20.3", "IEEE C57.12.00", "UL 1558", "UL 1778", "EIA-310"],
    "features": [
        "remote racking",
        "infrared windows",
        "seismic certified",
        "zone selective interlocking",
        "arc flash maintenance mode",
        "drawout breakers",
        "ventilated enclosure",
        "seal-off bushings",
        "expansion joints",
        "dry air pressurization",
        "space heaters",
        "flexible connections",
        "revenue metering",
        "utility disconnect",
        "maintenance bypass",
        "hot-swappable modules",
    ],
}

# Multiply by this number to convert to the catalog's unit.
UNIT_FACTORS = {
    "voltage_kv": {"kv": 1, "v": 0.001},
    "bil_kv": {"kv": 1},
    "bus_current_a": {"a": 1, "ka": 1000},
    "short_circuit_ka": {"ka": 1, "a": 0.001},
    "momentary_ka": {"ka": 1, "a": 0.001},
    "frequency_hz": {"hz": 1},
    "control_voltage_vdc": {"v": 1, "vdc": 1},
    "max_altitude_m": {"m": 1, "ft": 0.3048},
    "lead_time_weeks": {"weeks": 1, "week": 1},
    "max_ambient_c": {"c": 1},
    "price_usd": {"usd": 1, "$": 1, "dollars": 1},
    "power_kva": {"kva": 1, "mva": 1000},
    "power_kw": {"kw": 1, "mw": 1000},
    "secondary_voltage_kv": {"kv": 1, "v": 0.001},
    "impedance_pct": {"%": 1, "percent": 1},
    "runtime_min": {"min": 1, "minutes": 1},
    "efficiency_pct": {"%": 1, "percent": 1},
    "rack_units": {"u": 1, "ru": 1},
    "rack_power_kw": {"kw": 1},
    "static_load_kg": {"kg": 1, "lb": 0.45359237},
    "rack_width_mm": {"mm": 1},
}


def to_catalog_unit(parameter: str, value: float, unit: str) -> Optional[float]:
    """Convert a value to the catalog's unit. Returns None for an unknown unit."""
    clean = unit.strip().lower().replace("°", "")
    if parameter == "max_ambient_c" and clean == "f":
        return (value - 32) * 5 / 9
    factor = UNIT_FACTORS.get(parameter, {}).get(clean)
    return None if factor is None else value * factor


def _simple(text: str) -> str:
    """Lowercase text and remove punctuation so small differences do not matter."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _flatten(text: str) -> str:
    """Remove line breaks, repeated spaces, and fancy dashes from PDF text."""
    text = text.replace("–", "-").replace("—", "-").replace("‑", "-")
    return re.sub(r"\s+", " ", text).strip().lower()


def _numbers_in(text: str) -> list[float]:
    return [float(n.replace(",", "")) for n in re.findall(r"\d[\d,]*(?:\.\d+)?", text)]


def verify_source(req: Requirement, spec_text: str) -> Optional[str]:
    """Check Claude's work against the spec. Returns a problem, or None if it looks right."""
    if not req.source_quote.strip():
        return "No source quote was given."
    if _flatten(req.source_quote) not in _flatten(spec_text):
        return "The source quote was not found in the spec."
    if req.value_number is not None and req.value_number not in _numbers_in(req.source_quote):
        return "The value was not found in the source quote."
    return None


def _format(value, unit: str = "") -> str:
    if value is None:
        return "Not listed"
    if value == []:
        return "None"
    if isinstance(value, list):
        return ", ".join(_format(v, unit) for v in value)
    if isinstance(value, float):
        value = f"{value:.4g}"
    return f"{value} {unit}".strip()


def _required_text(req: Requirement) -> str:
    rule = RULES.get(req.parameter)
    if req.value_number is not None:
        word = {"min": "at least", "max": "at most"}.get(rule.mode, "") if rule else ""
        return f"{word} {req.value_number:g} {req.unit}".strip()
    return req.value_text or "See spec"


def check_requirement(req: Requirement, product: dict, spec_text: Optional[str] = None) -> CheckResult:
    rule = RULES.get(req.parameter)
    required = _required_text(req)

    def result(status, note="", value="Not checked"):
        source_problem = verify_source(req, spec_text) if spec_text is not None else None
        if source_problem:  # A bad source overrides any pass or fail.
            status, note = "REVIEW", f"{source_problem} {note}".strip()
        return CheckResult(requirement=req, required=required, product_value=value, status=status, note=note)

    if rule is None:
        return result("REVIEW", "This item is outside the automatic checks. An engineer must review it.")

    actual = product.get(req.parameter)
    shown = _format(actual, rule.unit)
    if actual is None:  # Unknown. An empty list means the product does not have it.
        return result("REVIEW", "The catalog has no value for this item.", shown)

    if rule.mode == "one_of_text":
        if not req.value_text:
            return result("REVIEW", "No required value was found.", shown)
        known = [_simple(v) for v in VOCABULARY[req.parameter]]
        if _simple(req.value_text) not in known:
            return result("REVIEW", "This value is not one the tool knows.", shown)
        listed = [_simple(v) for v in actual]
        return result("PASS" if _simple(req.value_text) in listed else "FAIL", "", shown)

    if req.value_number is None:
        return result("REVIEW", "No required value was found.", shown)
    needed = to_catalog_unit(req.parameter, req.value_number, req.unit)
    if needed is None:
        return result("REVIEW", f"Unknown unit: '{req.unit or 'none'}'.", shown)

    if rule.mode == "min":
        ok = actual >= needed
    elif rule.mode == "max":
        ok = actual <= needed
    else:
        ok = any(abs(needed - value) < 1e-6 for value in actual)
    return result("PASS" if ok else "FAIL", "", shown)


def check_product(requirements: list[Requirement], product: dict, spec_text: Optional[str] = None) -> ProductCheck:
    results = [check_requirement(r, product, spec_text) for r in requirements]
    return ProductCheck(product_id=product["id"], product_name=product["name"],
                        price_usd=product.get("price_usd"), results=results)


def rank_products(checks: list[ProductCheck]) -> list[ProductCheck]:
    """Best first. Ties go to the lower price, then to catalog order."""
    def price(c: ProductCheck) -> float:
        return c.price_usd if c.price_usd is not None else float("inf")

    return sorted(checks, key=lambda c: (c.mandatory_fails, c.reviews, c.preferred_misses, price(c)))
