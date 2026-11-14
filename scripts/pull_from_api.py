"""Pulls products from a company's product API and saves them as the SpecCheck catalog file.

Use this when you want a saved snapshot instead of live data (for example, to check it before use).

    PRODUCT_API_URL=https://api.example.com/v1/products PRODUCT_API_KEY=... python -m scripts.pull_from_api

The key is read from the environment or .env, never from this file.
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))
from speccheck.api_catalog import enabled, load_from_api  # noqa: E402

OUT = Path(__file__).parent.parent / "data" / "catalog_company.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(OUT), help="Where to save the catalog file")
    args = parser.parse_args()
    load_dotenv()
    if not enabled():
        sys.exit("Set PRODUCT_API_URL first (in .env or your shell).")
    products = load_from_api()
    out = {"note": "Pulled from the company product API. For internal use under that company's terms.",
           "checked": date.today().isoformat(), "products": products}
    Path(args.out).write_text(json.dumps(out, indent=2), encoding="utf-8")
    counts = {}
    for p in products:
        counts[p["equipment_type"]] = counts.get(p["equipment_type"], 0) + 1
    print(f"Saved {len(products)} products to {args.out}: {counts}")


if __name__ == "__main__":
    main()
