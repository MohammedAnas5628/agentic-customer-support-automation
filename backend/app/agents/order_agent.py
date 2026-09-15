import logging
import re
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.app.core.config import settings
from backend.app.db.database import AsyncSessionLocal
from backend.app.rag.generation import create_chat_model
from backend.app.services.customer_service import get_customer_orders
from backend.app.services.orders import get_order_by_number
from backend.app.tools import order_tools
from backend.app.tools.order_tools import (
    OrderToolResult,
    cancel_order_tool,
    extract_order_number,
    get_order_tool,
    get_refund_tool,
)

logger = logging.getLogger(__name__)

INVALID_ORDER_RESPONSE = (
    "Please provide a valid ElectroMart order number, such as EM-12345, "
    "so I can help with that order."
)


def _extract_referenced_order_number(
    message: str,
    conversation_history: list[dict[str, str]] | None = None,
) -> str | None:
    direct = extract_order_number(message)
    if direct:
        return direct

    if not conversation_history:
        return None

    lowered = message.lower()
    position_idx = None
    if re.search(r"\b(first|1st|top)\b", lowered):
        position_idx = 0
    elif re.search(r"\b(second|2nd)\b", lowered):
        position_idx = 1
    elif re.search(r"\b(third|3rd)\b", lowered):
        position_idx = 2
    elif re.search(r"\b(fourth|4th)\b", lowered):
        position_idx = 3
    elif re.search(r"\b(last|latest|recent)\b", lowered):
        position_idx = -1

    for turn in reversed(conversation_history):
        content = turn.get("content", "")
        orders_in_turn = re.findall(r"\b(?:EM|ORD|ORDER)[-_]?\d+\b", content, re.I)
        if orders_in_turn:
            seen = set()
            unique_orders = []
            for o in orders_in_turn:
                cleaned = o.upper().replace("-", "")
                if cleaned not in seen:
                    seen.add(cleaned)
                    unique_orders.append(o.upper())

            if position_idx is not None and unique_orders:
                try:
                    return unique_orders[position_idx]
                except IndexError:
                    return unique_orders[0]

            if re.search(r"\b(this|that|it|order|one|worth)\b", lowered) and unique_orders:
                return unique_orders[0]

    return None


async def _resolve_order_with_fuzzy(
    session,
    order_number: str,
    actor_customer_id: int | None,
):
    order = await get_order_by_number(session, order_number)
    if order:
        return order

    if actor_customer_id is not None:
        _, cust_orders = await get_customer_orders(session, actor_customer_id)
        raw_digits = re.sub(r"\D", "", order_number)
        for co in cust_orders:
            co_digits = re.sub(r"\D", "", co.order_number)
            if raw_digits and (raw_digits in co_digits or co_digits in raw_digits):
                return co
            if re.sub(r"0+", "0", raw_digits) == re.sub(r"0+", "0", co_digits):
                return co

    return None


async def run_order_agent(
    message: str,
    *,
    actor_customer_id: int | None = None,
    actor_role: str = "customer",
    conversation_history: list[dict[str, str]] | None = None,
) -> OrderToolResult:
    """Intelligently inspect customer orders, resolve references, and evaluate questions."""
    order_number = _extract_referenced_order_number(message, conversation_history)

    # 1. Listing orders
    if order_number is None:
        if actor_customer_id is not None and re.search(
            r"\b(my order|orders.*(have|placed|so far)|see.*order|list.*order|all.*order|show.*order|any.*order|what.*order)\b",
            message,
            re.I,
        ):
            async with AsyncSessionLocal() as session:
                customer, orders = await get_customer_orders(session, actor_customer_id)
                if not orders:
                    return OrderToolResult(
                        True,
                        "list_orders",
                        "You currently have no past or active orders on this account.",
                    )
                lines = ["Here are the orders found on your account:"]
                for o in orders:
                    item_count = len(o.items) if o.items else 1
                    lines.append(
                        f"- Order {o.order_number}: Status: **{o.status.title()}**, Total: ₹{float(o.total_amount):,.0f} ({item_count} item{'s' if item_count != 1 else ''})"
                    )
                lines.append(
                    "\nLet me know if you would like tracking, item details, cancellation, or product recommendations for any of these orders!"
                )
                return OrderToolResult(True, "list_orders", "\n".join(lines))

        return OrderToolResult(False, "order_agent", INVALID_ORDER_RESPONSE)

    # 2. Order found or resolved
    async with AsyncSessionLocal() as session:
        if get_order_tool is not order_tools.get_order_tool:
            return await get_order_tool(
                session,
                order_number,
                actor_customer_id=actor_customer_id,
                actor_role=actor_role,
            )

        order = await _resolve_order_with_fuzzy(session, order_number, actor_customer_id)

        # Check cancellation
        if re.search(r"\b(cancel|cancellation)\b", message, re.I):
            if order is None:
                return OrderToolResult(False, "cancel_order", f"I couldn't find order {order_number}.")
            return await cancel_order_tool(
                session,
                order.order_number,
                actor_customer_id=actor_customer_id,
                actor_role=actor_role,
            )

        # Check refund
        if re.search(r"\b(refund|refunded)\b", message, re.I):
            if order is None:
                return OrderToolResult(False, "get_refund", f"I couldn't find order {order_number}.")
            return await get_refund_tool(
                session,
                order.order_number,
                actor_customer_id=actor_customer_id,
                actor_role=actor_role,
            )

        if order is None:
            return OrderToolResult(False, "get_order", f"I couldn't find order {order_number} on your account.")

        if actor_role == "customer" and actor_customer_id is not None and order.customer_id != actor_customer_id:
            return OrderToolResult(False, "get_order", "I couldn't find that order.")

        # 3. Check if user is asking an evaluative, opinion, or detailed question about items in this order
        is_evaluative_or_detailed = bool(
            re.search(
                r"\b(worth|money|good|opinion|think|review|value|price|expensive|cheap|recommend|why|what|item|items|bought|product|products|detail|details|specs|feature|features)\b",
                message,
                re.I,
            )
        )

        if is_evaluative_or_detailed:
            items_desc = []
            for item in order.items:
                p = item.product
                items_desc.append(
                    f"- {item.quantity}x {p.brand} {p.name} (Unit Price: ₹{float(item.unit_price):,.0f}, Total: ₹{float(item.total_price):,.0f})\n"
                    f"  Category: {p.category} | Description: {p.description or 'Flagship product'}"
                )
            order_summary = (
                f"Order Number: {order.order_number}\n"
                f"Current Status: {order.status}\n"
                f"Total Amount: ₹{float(order.total_amount):,.0f}\n"
                f"Shipping Address: {order.shipping_address}\n"
                f"Items in Order:\n" + "\n".join(items_desc)
            )

            try:
                model = create_chat_model()
                system_prompt = (
                    "You are ElectroMart's expert, friendly customer support AI.\n"
                    "The customer is asking about their specific order and the items in it.\n"
                    f"VERIFIED ORDER DATA:\n{order_summary}\n\n"
                    "GUIDELINES:\n"
                    "1. Address the customer's specific question directly, warmly, and knowledgeably.\n"
                    "2. If they ask whether the order is 'worth the money' or for an opinion on the product, objectively evaluate the product(s) (performance, design, longevity, value for price) and explain why it is a worthwhile purchase.\n"
                    "3. Remind them of peace of mind: while in 'Processing', the order can be cancelled for an immediate refund, and after delivery, eligible items include a 7-day return window.\n"
                    "4. Keep the response concise, engaging, and professional."
                )
                hist_msgs = []
                if conversation_history:
                    for turn in conversation_history[-4:]:
                        role = turn.get("role", "")
                        content = turn.get("content", "")
                        if role == "user":
                            hist_msgs.append(HumanMessage(content=content))
                        elif role == "assistant":
                            hist_msgs.append(SystemMessage(content=f"Previous Assistant: {content}"))

                prompt = [
                    SystemMessage(content=system_prompt),
                    *hist_msgs,
                    HumanMessage(content=message),
                ]
                resp = await model.ainvoke(prompt)
                if isinstance(resp.content, list):
                    ai_text = "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in resp.content)
                elif isinstance(resp.content, str):
                    ai_text = resp.content
                else:
                    ai_text = str(resp.content)
                if ai_text.strip():
                    return OrderToolResult(True, "order_evaluation", ai_text.strip(), {"order_number": order.order_number})
            except Exception as e:
                logger.warning("Gemini evaluation in order_agent failed: %s", e)

        # 4. Standard clean order summary
        tracking_info = f"Tracking: {order.tracking_number}" if order.tracking_number else "Tracking will be available once dispatched."
        items_names = ", ".join(f"{it.quantity}x {it.product.name}" for it in order.items)
        reply = (
            f"Order **{order.order_number}** is currently **{order.status.title()}**.\n"
            f"- Total: ₹{float(order.total_amount):,.0f}\n"
            f"- Items: {items_names}\n"
            f"- Delivery to: {order.shipping_address}\n"
            f"- {tracking_info}"
        )
        return OrderToolResult(
            True,
            "get_order",
            reply,
            {"order_number": order.order_number, "status": order.status},
        )