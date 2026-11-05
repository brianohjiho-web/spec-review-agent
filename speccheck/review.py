"""Turns requirements into a ranked review and a CSV export."""
import csv
from io import StringIO

from .catalog import by_type
from .checks import RULES, check_product, rank_products
from .models import ProductCheck, Review, SpecRequirements


def build_review(spec: SpecRequirements, catalog: list[dict], spec_text: str | None = None, **details) -> Review:
    checks = [check_product(spec.requirements, p, spec_text) for p in by_type(catalog, spec.equipment_type)]
    ranked = rank_products(checks)
    best = ranked[0] if ranked else None
    # Python picks the product. A product with a mandatory failure is never recommended.
    recommended = best.product_id if best and best.mandatory_fails == 0 else None
    return Review(equipment_type=spec.equipment_type, ranked=ranked, recommended_id=recommended, **details)


def _safe_cell(value: str) -> str:
    """Stop spreadsheet apps from running spec text as a formula."""
    return f"'{value}" if value[:1] in ("=", "+", "-", "@", "\t", "\r") else value


def to_csv(check: ProductCheck) -> str:
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Section", "Item", "Mandatory", "Required", "Product", "Status", "Note", "Source quote"])
    for r in check.results:
        req = r.requirement
        rule = RULES.get(req.parameter)
        label = rule.label if rule else "Other"
        row = [req.id, req.section, label, "Yes" if req.mandatory else "No", r.required,
               r.product_value, r.status, r.note, req.source_quote]
        writer.writerow([_safe_cell(str(cell)) for cell in row])
    return output.getvalue()
