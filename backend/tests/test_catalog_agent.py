from decimal import Decimal
from types import SimpleNamespace

import pytest

from backend.app.agents import catalog_agent


def _product(sku: str, name: str, brand: str, category: str, price: str, active: bool = True):
    return SimpleNamespace(
        sku=sku,
        name=name,
        brand=brand,
        category=category,
        price=Decimal(price),
        is_active=active,
    )


class FakeSession:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return False


@pytest.mark.asyncio
async def test_laptop_query_uses_catalog_and_excludes_inactive(monkeypatch):
    products = [_product("EM-LT-001", "Inspiron 15", "Dell", "Laptops", "64999"), _product("EM-LT-999", "Hidden", "Dell", "Laptops", "1", False)]
    async def search(_session, **_filters):
        return products

    monkeypatch.setattr(catalog_agent, "search_products", search)
    answer = await catalog_agent.run_catalog_agent("Suggest me a laptop", FakeSession())

    assert "Dell Inspiron 15" in answer
    assert "Hidden" not in answer
    assert "₹64,999" in answer


@pytest.mark.asyncio
async def test_all_products_are_grouped_from_real_records(monkeypatch):
    products = [_product("EM-LT-001", "Inspiron 15", "Dell", "Laptops", "64999"), _product("EM-PH-001", "Galaxy S26", "Samsung", "Smartphones", "74999")]
    async def get_all(_session):
        return products

    monkeypatch.setattr(catalog_agent, "get_products", get_all)
    answer = await catalog_agent.run_catalog_agent("Give me all your products", FakeSession())

    assert "Laptops" in answer and "Smartphones" in answer
    assert "Dell Inspiron 15" in answer and "Samsung Galaxy S26" in answer


@pytest.mark.asyncio
async def test_no_matching_product_is_explicit(monkeypatch):
    async def search(_session, **_filters):
        return []

    monkeypatch.setattr(catalog_agent, "search_products", search)
    answer = await catalog_agent.run_catalog_agent("Do you have cameras?", FakeSession())

    assert "couldn't find" in answer.lower()
    assert "camera" not in answer.lower().replace("cameras", "")