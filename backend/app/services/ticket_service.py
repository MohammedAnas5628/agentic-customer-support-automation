from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.models.customer import Customer
from backend.app.models.order import Order
from backend.app.models.ticket import Ticket


async def get_ticket_by_number(
    session: AsyncSession,
    ticket_number: str,
) -> Ticket | None:
    statement = (
        select(Ticket)
        .where(Ticket.ticket_number == ticket_number)
        .options(
            selectinload(Ticket.customer),
            selectinload(Ticket.order),
        )
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_customer(
    session: AsyncSession,
    customer_id: int,
) -> Customer | None:
    statement = select(Customer).where(Customer.id == customer_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_order_by_number(
    session: AsyncSession,
    order_number: str,
) -> Order | None:
    statement = select(Order).where(Order.order_number == order_number)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def generate_ticket_number(session: AsyncSession) -> str:
    while True:
        ticket_number = f"TKT{uuid4().hex[:12].upper()}"
        statement = select(Ticket.id).where(Ticket.ticket_number == ticket_number)
        result = await session.execute(statement)
        if result.scalar_one_or_none() is None:
            return ticket_number


async def create_ticket(
    session: AsyncSession,
    *,
    customer_id: int,
    order_number: str | None,
    subject: str,
    description: str,
    status: str,
    priority: str,
) -> Ticket | None:
    customer = await get_customer(session, customer_id)
    if customer is None:
        return None

    order = None
    if order_number is not None:
        order = await get_order_by_number(session, order_number)
        if order is None or order.customer_id != customer_id:
            return None

    ticket = Ticket(
        ticket_number=await generate_ticket_number(session),
        customer_id=customer_id,
        order_id=order.id if order else None,
        subject=subject,
        description=description,
        status=status,
        priority=priority,
    )
    session.add(ticket)
    await session.commit()
    return await get_ticket_by_number(session, ticket.ticket_number)


async def update_ticket(
    session: AsyncSession,
    ticket_number: str,
    changes: dict[str, str],
) -> Ticket | None:
    ticket = await get_ticket_by_number(session, ticket_number)
    if ticket is None:
        return None

    for field, value in changes.items():
        setattr(ticket, field, value)

    await session.commit()
    return await get_ticket_by_number(session, ticket_number)