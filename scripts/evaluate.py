"""Scores SpecCheck on the sample specs.

Saved mode:  python scripts/evaluate.py
             Checks the Python rules using hand-labeled requirements.
Live mode:   python scripts/evaluate.py --live
             Sends each PDF to Claude and scores what it extracts. Uses API credits.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

from speccheck.agent import SpecAgent
from speccheck.catalog import load_catalog
from speccheck.checks import to_catalog_unit
from speccheck.models import SpecRequirements
from speccheck.pdf import read_pdf
from speccheck.review import build_review
from speccheck.settings import has_api_key

SAMPLES = ROOT / "data" / "samples"


def key(req):
    """A comparable label for one requirement, with the unit converted."""
    if req.value_number is not None:
        value = to_catalog_unit(req.parameter, req.value_number, req.unit)
        value = round(value, 2) if value is not None else f"{req.value_number} {req.unit}"
    else:
        value = (req.value_text or "").lower() if req.parameter != "other" else ""
    return (req.parameter, value)


def score_extraction(found, labels):
    found_keys = {key(r) for r in found.requirements}
    label_keys = {key(r) for r in labels.requirements}
    right = len(found_keys & label_keys)
    return {
        "right": right,
        "found": len(found_keys),
        "labeled": len(label_keys),
        "missed": sorted(map(str, label_keys - found_keys)),
        "extra": sorted(map(str, found_keys - label_keys)),
    }


def review_matches(review, expected):
    top = review.ranked[0]
    fails = sorted(r.requirement.parameter for r in top.results
                   if r.status == "FAIL" and r.requirement.mandatory)
    return (review.recommended_id == expected["recommended"]
            and top.product_id == expected["top_ranked"]
            and fails == sorted(expected["top_ranked_fails"]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="Use Claude. This uses API credits.")
    args = parser.parse_args()
    load_dotenv(ROOT / ".env")
    if args.live and not has_api_key():
        sys.exit("Add your ANTHROPIC_API_KEY to the .env file first.")

    catalog = load_catalog()
    passed, right, found, labeled = 0, 0, 0, 0
    pdfs = sorted(SAMPLES.glob("*.pdf"))

    for pdf in pdfs:
        name = pdf.stem
        spec_text = read_pdf(pdf.read_bytes())
        labels = SpecRequirements(**json.loads((SAMPLES / f"{name}.requirements.json").read_text()))
        expected = json.loads((SAMPLES / f"{name}.expected.json").read_text())

        if args.live:
            agent = SpecAgent(catalog)
            review = agent.run(spec_text)
            score = score_extraction(agent.spec, labels)
            right += score["right"]
            found += score["found"]
            labeled += score["labeled"]
            print(f"{name}: {score['right']}/{score['labeled']} labeled items found")
            if score["missed"]:
                print(f"  missed: {score['missed']}")
            if score["extra"]:
                print(f"  extra: {score['extra']}")
        else:
            review = build_review(labels, catalog, spec_text)

        ok = review_matches(review, expected)
        passed += ok
        print(f"{name}: recommendation {'correct' if ok else 'WRONG'} ({review.recommended_id or 'no compliant product'})")

    print(f"\nRecommendations correct: {passed}/{len(pdfs)}")
    if args.live:
        print(f"Recall: {right / labeled:.0%}  Precision: {right / found if found else 0:.0%}")


if __name__ == "__main__":
    main()
