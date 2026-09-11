import re
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.services.order_cancellation import cancel_order as cancel_order_service
from backend.app.services.orders import get_order_by_number
from backend.app.services.refund_service import get_order_with_refund


ORDER_NUMBER_PATTERN = re.compile(r"\b(?:EM|ORD|ORDER)[-_]?\d+\b", re.IGNORECASE)
ELIGIBLE_CANCELLATION_STATUSES = frozenset({"processing", "packed"})


@dataclass(frozen=True)
class OrderToolResult:
    success: bool
    tool: str
    message: str
    data: dict[str, object] | None = None


def extract_order_number(message: str) -> str | None:
    match = ORDER_NUMBER_PATTERN.search(message)
    return match.group(0).upper() if match else None


async def get_order_tool(
    session: AsyncSession,
    order_number: str,
    *,
    actor_customer_id: int | None = None,
    actor_role: str = "customer",
) -> OrderToolResult:
    order = await get_order_by_number(session, order_number)
    if order is None or (
        actor_role == "customer"
        and actor_customer_id is not None
        and order.customer_id != actor_customer_id
    ):
        return OrderToolResult(False, "get_order", "I couldn't find that order.")
    return OrderToolResult(
        True,
        "get_order",
        f"Order {order.order_number} is currently {order.status}.",
        {"order_number": order.order_number, "status": order.status},
    )


async def get_refund_tool(
    session: AsyncSession,
    order_number: str,
    *,
    actor_customer_id: int | None = None,
    actor_role: str = "customer",
) -> OrderToolResult:
    order = await get_order_with_refund(session, order_number)
    if order is None or (
        actor_role == "customer"
        and actor_customer_id is not None
        and order.customer_id != actor_customer_id
    ):
        return OrderToolResult(False, "get_refund", "I couldn't find that order.")

    payment = order.payment
    refund = payment.refunds[0] if payment and payment.refunds else None
    if refund is None:
        return OrderToolResult(
            True,
            "get_refund",
            f"No refund is recorded for order {order.order_number}.",
            {"order_number": order.order_number, "refund_status": None},
        )
    return OrderToolResult(
        True,
        "get_refund",
        f"The refund for order {order.order_number} is {refund.refund_status}.",
        {
            "order_number": order.order_number,
            "refund_status": refund.refund_status,
            "refund_amount": str(refund.amount),
        },
    )


async def cancel_order_tool(
    session: AsyncSession,
    order_number: str,
    *,
    actor_customer_id: int | None = None,
    actor_role: str = "customer",
) -> OrderToolResult:
    if actor_role == "customer" and actor_customer_id is not None:
        order_check = await get_order_by_number(session, order_number)
        if order_check is None or order_check.customer_id != actor_customer_id:
            return OrderToolResult(False, "cancel_order", "I couldn't find that order.")
    order, previous_status = await cancel_order_service(session, order_number)
    if order is None or previous_status is None:
        return OrderToolResult(False, "cancel_order", "I couldn't find that order.")
    if previous_status not in ELIGIBLE_CANCELLATION_STATUSES:
        return OrderToolResult(
            False,
            "cancel_order",
            f"I cannot cancel the order because its status is '{previous_status}'.",
            {"order_number": order.order_number, "status": previous_status},
        )
    return OrderToolResult(
        True,
        "cancel_order",
        f"Order {order.order_number} was cancelled successfully.",
        {
            "order_number": order.order_number,
            "previous_status": previous_status,
            "new_status": order.status,
        },
    )