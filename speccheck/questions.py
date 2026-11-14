"""Builds plain questions to ask the customer and your own engineers after a review.

Each side gets a fixed "every job" list that never changes, plus a short
"from this spec" list: failed or unclear items first, then questions for the
equipment family.
"""
import json
from pathlib import Path

from .checks import RULES
from .models import Review

QUESTIONS = json.loads((Path(__file__).parent.parent / "data" / "questions.json").read_text(encoding="utf-8"))
SPEC_LIMIT = 3


def _item(result) -> str:
    rule = RULES.get(result.requirement.parameter)
    return rule.label if rule else "Other"


def make_questions(review: Review) -> dict[str, list[str]]:
    best = review.ranked[0] if review.ranked else None
    family = QUESTIONS["families"].get(review.equipment_type, "")
    customer = list(review.customer_questions)
    engineer = []
    for r in best.results if best else []:
        item, quote = _item(r), r.requirement.source_quote
        if r.status == "FAIL":
            customer.append(f"{item}: the spec asks for {r.required}, but our closest product has {r.product_value}. "
                            "Is this a firm limit, or could ours work?")
            engineer.append(f"{item}: can {best.product_name} be changed to meet {r.required}? "
                            "What would it add in cost and weeks?")
        elif r.status != "REVIEW":
            continue
        elif "outside the automatic checks" in r.note:
            engineer.append(f"The spec says \u201c{quote}\u201d. Can we meet this, and does it change the price?")
        elif "no value" in r.note or "public page" in r.note:
            # The spec is clear; our own product data is missing. Ask our side, not the customer.
            need = r.required.replace("at least ", "").replace("at most ", "")
            engineer.append(f"{item}: the spec asks for {need}, but our product data doesn't say. "
                            "Can we confirm ours meets it?")
        else:
            customer.append(f"{item}: the spec says \u201c{quote}\u201d. Can you confirm the exact value you need?")
    customer += QUESTIONS["customer"].get(family, [])
    engineer += QUESTIONS["engineer"].get(family, [])
    return {
        "customer_fixed": QUESTIONS["customer"]["every_job"],
        "engineer_fixed": QUESTIONS["engineer"]["every_job"],
        "customer": customer[:SPEC_LIMIT],
        "engineer": engineer[:SPEC_LIMIT],
    }
