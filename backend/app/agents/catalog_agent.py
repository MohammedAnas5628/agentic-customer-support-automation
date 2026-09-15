import logging
import re
from contextlib import asynccontextmanager
from typing import AsyncIterator

from backend.app.db.database import AsyncSessionLocal
from backend.app.models.product import Product
from backend.app.services.product_service import get_products, search_products

logger = logging.getLogger(__name__)

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


def _extract_max_price(question: str) -> float | None:
    match = re.search(r"\b(?:under|below|less than|within|max(?:imum)?)\s*(?:rs\.?|inr|₹)?\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(k)?\b", question, re.I)
    if match:
        val = float(match.group(1).replace(",", ""))
        if match.group(2):
            val *= 1000
        return val
    return None


def _format_products(products: list[Product], question: str) -> str:
    if not products:
        return "I couldn't find a matching ElectroMart product in the current catalog."
    category = _query_category(question)
    if _ALL_PRODUCTS.search(question) and category is None:
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


async def run_catalog_agent(
    question: str,
    session=None,
    conversation_history: list[dict[str, str]] | None = None,
) -> str:
    """Answer product questions from the live catalog, respecting categories, budgets, and conversation history."""
    async with _session_scope(session) as active_session:
        category = _query_category(question)
        max_price = _extract_max_price(question)

        # Handle follow-up questions referencing previous conversation
        is_followup = bool(
            conversation_history
            and re.search(r"\b(those|these|that|them|it|explain|tell me more|more about|compare|difference|which one|first one|second one|cheapest|recommend|suggest)\b", question, re.I)
        )

        if is_followup:
            try:
                from backend.app.rag.generation import create_chat_model, _response_text
                from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

                all_prods = [p for p in await get_products(active_session) if p.is_active]
                catalog_summary = "\n".join(
                    f"- {_product_label(p)} ({p.category}): {_format_price(p.price)} — {p.description or 'In stock'}"
                    for p in all_prods
                )
                hist_msgs = []
                for h in (conversation_history or [])[-6:]:
                    if h.get("role") == "user":
                        hist_msgs.append(HumanMessage(content=h["content"]))
                    elif h.get("role") == "assistant":
                        hist_msgs.append(AIMessage(content=h["content"]))

                model = create_chat_model()
                prompt = [
                    SystemMessage(
                        content=(
                            "You are the ElectroMart Product Specialist.\n"
                            f"Below is our active product catalog:\n{catalog_summary}\n\n"
                            "Answer the customer's question directly, clearly, and concisely using the products listed above.\n"
                            "If comparing or explaining products mentioned previously, explain their key specs, benefits, and price differences accurately."
                        )
                    ),
                    *hist_msgs,
                    HumanMessage(content=question),
                ]
                resp = await model.ainvoke(prompt)
                ans = _response_text(resp.content).strip()
                if ans:
                    return ans
            except Exception as e:
                logger.warning("Gemini follow-up generation in catalog agent failed: %s", e)

        # Regular product search
        if category is not None:
            products = [product for product in await search_products(active_session, category=category) if product.is_active]
        elif _ALL_PRODUCTS.search(question):
            products = [product for product in await get_products(active_session) if product.is_active]
        elif _UNSUPPORTED_CATEGORY.search(question) and category is None:
            products = []
        else:
            all_prods = [product for product in await get_products(active_session) if product.is_active]
            keywords = [w for w in re.findall(r"\w+", question.lower()) if len(w) > 2 and w not in {"the", "and", "show", "can", "you", "for", "with"}]
            matching = [p for p in all_prods if any(k in p.name.lower() or (p.description and k in p.description.lower()) for k in keywords)]
            products = matching if matching else all_prods

        # Apply price constraint if specified
        if max_price is not None:
            filtered = [p for p in products if float(p.price) <= max_price]
            if not filtered and products:
                lowest = min(products, key=lambda p: float(p.price))
                label = category.lower() if category else "options"
                return (
                    f"We do not currently have {label} under ₹{max_price:,.0f} in our catalog. "
                    f"Our available options start at {_format_price(lowest.price)} ({_product_label(lowest)}). "
                    "Would you like more details on that?"
                )
            products = filtered

        return _format_products(products, question)