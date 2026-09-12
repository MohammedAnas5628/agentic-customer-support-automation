import re
from contextlib import asynccontextmanager
from typing import AsyncIterator

from backend.app.db.database import AsyncSessionLocal
from backend.app.models.product import Product
from backend.app.services.product_service import get_products, search_products


_CATEGORY_TERMS = {
    "laptop": "Laptops",
    "notebook": "Laptops",
    "mobile": "Smartphones",
    "phone": "Smartphones",
    "smartphone": "Smartphones",
    "tablet": "Tablets",
    "headphone": "Headphones",
    "earbud": "Headphones",
    "watch": "Smartwatches",
    "smartwatch": "Smartwatches",
    "television": "Electronics",
    "tv": "Electronics",
    "gaming": "Gaming",
    "console": "Gaming",
    "charger": "Accessories",
    "cable": "Accessories",
    "keyboard": "Accessories",
    "mouse": "Accessories",
    "accessor": "Accessories",
}
_ALL_PRODUCTS = re.compile(r"\b(all|every|entire|list|catalog|what do you (sell|have)|what products)\b", re.I)
_UNSUPPORTED_CATEGORY = re.compile(r"\b(camera|cameras|speaker|speakers|soundbar|projector|projectors|desktop|desktops|fitness band|fitness bands|appliance|appliances)\b", re.I)


def _format_price(price: object) -> str:
    return f"₹{float(price):,.0f}"


def _product_label(product: Product) -> str:
    name = product.name
    return name if name.lower().startswith(product.brand.lower()) else f"{product.brand} {name}"


def _query_category(question: str) -> str | None:
    lowered = question.lower()
    for term, category in _CATEGORY_TERMS.items():
        if re.search(rf"\b{re.escape(term)}\w*\b", lowered):
            return category
    return None


def _format_products(products: list[Product], question: str) -> str:
    if not products:
        return "I couldn't find a matching ElectroMart product in the current catalog."
    category = _query_category(question)
    if _ALL_PRODUCTS.search(question):
        groups: dict[str, list[Product]] = {}
        for product in products:
            groups.setdefault(product.category, []).append(product)
        lines = ["Here are the products currently in the ElectroMart catalog:"]
        for group, items in groups.items():
            lines.append(f"\n{group}")
            lines.extend(f"- {_product_label(item)} — {_format_price(item.price)}" for item in items)
        return "\n".join(lines)
    label = category.lower() if category else "matching products"
    lines = [f"Here are the {label} currently available in the ElectroMart catalog:"]
    lines.extend(f"- {_product_label(item)} — {_format_price(item.price)}" for item in products)
    return "\n".join(lines) + "\nWould you like help comparing these options?"


@asynccontextmanager
async def _session_scope(session=None) -> AsyncIterator[object]:
    if session is not None:
        yield session
        return
    async with AsyncSessionLocal() as managed_session:
        yield managed_session


async def run_catalog_agent(question: str, session=None) -> str:
    """Answer product questions from the live catalog only."""
    async with _session_scope(session) as active_session:
        if _ALL_PRODUCTS.search(question):
            products = [product for product in await get_products(active_session) if product.is_active]
        elif _UNSUPPORTED_CATEGORY.search(question) and _query_category(question) is None:
            products = []
        else:
            products = [product for product in await search_products(active_session, category=_query_category(question)) if product.is_active]
    return _format_products(products, question)