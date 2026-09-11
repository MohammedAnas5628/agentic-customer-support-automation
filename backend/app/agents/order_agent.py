import re

from backend.app.db.database import AsyncSessionLocal
from backend.app.tools.order_tools import (
    OrderToolResult,
    cancel_order_tool,
    extract_order_number,
    get_order_tool,
    get_refund_tool,
)


INVALID_ORDER_RESPONSE = (
    "Please provide a valid ElectroMart order number, such as EM-12345, "
    "so I can help with that order."
)


def _requested_tool(message: str):
    lowered = message.lower()
    if re.search(r"\b(cancel|cancellation)\b", lowered):
        return cancel_order_tool
    if re.search(r"\b(refund|refunded|refunds)\b", lowered):
        return get_refund_tool
    return get_order_tool


async def run_order_agent(
    message: str,
    *,
    actor_customer_id: int | None = None,
    actor_role: str = "customer",
) -> OrderToolResult:
    """Choose an order tool, then delegate validation and DB access to it."""
    order_number = extract_order_number(message)
    if order_number is None:
        return OrderToolResult(False, "order_agent", INVALID_ORDER_RESPONSE)

    tool = _requested_tool(message)
    async with AsyncSessionLocal() as session:
        return await tool(
            session,
            order_number,
            actor_customer_id=actor_customer_id,
            actor_role=actor_role,
        )