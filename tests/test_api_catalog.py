import json
import pytest

from speccheck import api_catalog


def test_maps_fields_and_skips_other_types():
    items = [
        {"sku": "X-15", "name": "Gear 15", "manufacturer": "Acme", "category": "Medium Voltage Switchgear",
         "max_voltage_kv": 15, "continuous_current_a": 2000, "standards": "IEEE C37.20.2, UL", "location": "indoor"},
        {"sku": "M-1", "name": "Motor", "category": "motor"},
        {"name": "No id", "category": "ups"},
    ]
    products = [p for p in map(api_catalog.to_product, items) if p]
    assert len(products) == 1
    p = products[0]
    assert p["equipment_type"] == "mv_switchgear" and p["voltage_kv"] == 15 and p["bus_current_a"] == 2000
    assert p["standards"] == ["IEEE C37.20.2", "UL"] and p["location"] == ["indoor"]
    assert p["lists_complete"] is True


def test_follows_pages_and_sends_key(monkeypatch):
    seen = []

    class Resp:
        def __init__(self, body): self.body = body
        def read(self): return json.dumps(self.body).encode()
        def __enter__(self): return self
        def __exit__(self, *a): return False

    def fake_open(req, timeout):
        seen.append((req.full_url, req.get_header("Authorization")))
        if req.full_url.endswith("page=2"):
            return Resp({"products": [{"sku": "B"}]})
        return Resp({"products": [{"sku": "A"}], "next": "/v1/products?page=2"})

    monkeypatch.setattr(api_catalog.urllib.request, "urlopen", fake_open)
    items = api_catalog.fetch_items("https://api.example.com/v1/products", key="k123")
    assert [i["sku"] for i in items] == ["A", "B"]
    assert seen[1][0] == "https://api.example.com/v1/products?page=2"
    assert all(h == "Bearer k123" for _, h in seen)


def test_refuses_cross_origin_pagination_with_key(monkeypatch):
    class Resp:
        def read(self): return json.dumps({"products": [], "next": "https://attacker.example/steal"}).encode()
        def __enter__(self): return self
        def __exit__(self, *a): return False

    monkeypatch.setattr(api_catalog.urllib.request, "urlopen", lambda *a, **k: Resp())
    with pytest.raises(ValueError, match="changed origin"):
        api_catalog.fetch_items("https://api.example.com/v1/products", key="secret")


def test_off_by_default(monkeypatch):
    monkeypatch.delenv("PRODUCT_API_URL", raising=False)
    assert not api_catalog.enabled()
