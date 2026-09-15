import re
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.order import Order


async def cancel_order(
    session: AsyncSession,
    order_number: str,
) -> tuple[Order | None, str | None]:
    clean = re.sub(r"[-_\s]", "", order_number).upper()
    digits = re.sub(r"\D", "", order_number)
    conditions = [
        Order.order_number.ilike(order_number.strip()),
        Order.order_number.ilike(clean),
    ]
    if digits:
        conditions.extend([
            Order.order_number.ilike(f"EM{digits}"),
            Order.order_number.ilike(f"EM-{digits}"),
            Order.order_number.ilike(f"ORD-{digits}"),
        ])

    statement = (
        select(Order)
        .where(or_(*conditions))
        .with_for_update()
    )
    result = await session.execute(statement)
    order = result.scalar_one_or_none()
    if order is None:
        return None, None

    previous_status = order.status
    if previous_status not in {"processing", "packed"}:
        await session.commit()
        return order, previous_status

    order.status = "cancelled"
    await session.commit()
    return order, previous_status