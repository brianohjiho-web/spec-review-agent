from speccheck.metals import LB_PER_METRIC_TON, history_from_csv, material_cost, saved_prices


def test_reads_history_and_skips_missing():
    csv_text = "observation_date,PCOPPUSDM\n2026-08-01,14331.26\n2026-09-01,14473.06\n2026-10-01,.\n"
    assert history_from_csv(csv_text) == [["2026-08-01", 14331.26], ["2026-09-01", 14473.06]]


def test_live_and_entered_costs():
    prices = {"copper": {"history": [["d", LB_PER_METRIC_TON * 5]]}}
    rows = material_cost({"copper": 100, "steel": 50, "transformer_oil": 10}, prices, {"steel": 0.5})
    by_key = {r["key"]: r for r in rows}
    assert round(by_key["copper"]["cost"]) == 500
    assert by_key["steel"]["cost"] == 25
    assert by_key["transformer_oil"]["cost"] is None and by_key["transformer_oil"]["unit"] == "gal"


def test_saved_prices_have_a_year_of_history():
    prices = saved_prices()
    assert set(prices) == {"copper", "aluminum", "lead", "nickel", "steel", "electrical_steel", "transformer_oil", "brent"}
    assert all(len(p["history"]) == 13 for p in prices.values())


def test_typed_price_replaces_fred_price():
    prices = {"copper": {"history": [["d", LB_PER_METRIC_TON * 5]]}}
    row = material_cost({"copper": 100}, prices, {"copper": 2})[0]
    assert row["cost"] == 200 and row["source"] == "entered"
