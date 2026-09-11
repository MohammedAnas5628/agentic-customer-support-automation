from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.models.order import Order
from backend.app.models.payment import Payment


async def get_order_with_refund(
    session: AsyncSession,
    order_number: str,
) -> Order | None:
    statement = (
        select(Order)
        .where(Order.order_number == order_number)
        .options(selectinload(Order.payment).selectinload(Payment.refunds))
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()