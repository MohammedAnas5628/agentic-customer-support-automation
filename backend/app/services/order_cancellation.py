from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.order import Order


async def cancel_order(
    session: AsyncSession,
    order_number: str,
) -> tuple[Order | None, str | None]:
    statement = (
        select(Order)
        .where(Order.order_number == order_number)
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