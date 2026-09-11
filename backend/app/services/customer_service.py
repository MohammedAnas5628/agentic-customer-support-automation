from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.models.customer import Customer
from backend.app.models.order import Order
from backend.app.models.order_item import OrderItem
from backend.app.models.payment import Payment
from backend.app.models.ticket import Ticket


async def get_customer(
    session: AsyncSession,
    customer_id: int,
) -> Customer | None:
    statement = select(Customer).where(Customer.id == customer_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_customer_orders(
    session: AsyncSession,
    customer_id: int,
) -> tuple[Customer | None, list[Order]]:
    customer = await get_customer(session, customer_id)
    if customer is None:
        return None, []

    statement = (
        select(Order)
        .where(Order.customer_id == customer_id)
        .options(
            selectinload(Order.customer),
            selectinload(Order.items).selectinload(OrderItem.product),
            selectinload(Order.payment).selectinload(Payment.refunds),
        )
        .order_by(Order.created_at.desc())
    )
    result = await session.execute(statement)
    return customer, list(result.scalars().all())


async def get_customer_tickets(
    session: AsyncSession,
    customer_id: int,
) -> tuple[Customer | None, list[Ticket]]:
    customer = await get_customer(session, customer_id)
    if customer is None:
        return None, []

    statement = (
        select(Ticket)
        .where(Ticket.customer_id == customer_id)
        .options(selectinload(Ticket.order))
        .order_by(Ticket.created_at.desc())
    )
    result = await session.execute(statement)
    return customer, list(result.scalars().all())