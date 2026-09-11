from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.schemas.customer import (
    CustomerResponse,
    CustomerTicketResponse,
)
from backend.app.schemas.order import OrderResponse
from backend.app.services.customer_service import (
    get_customer,
    get_customer_orders,
    get_customer_tickets,
)


router = APIRouter(prefix="/api/customers", tags=["customers"])


@router.get("/{customer_id}", response_model=CustomerResponse)
async def read_customer(
    customer_id: int,
    session: AsyncSession = Depends(get_db),
) -> CustomerResponse:
    customer = await get_customer(session, customer_id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return customer


@router.get("/{customer_id}/orders", response_model=list[OrderResponse])
async def read_customer_orders(
    customer_id: int,
    session: AsyncSession = Depends(get_db),
) -> list[OrderResponse]:
    customer, orders = await get_customer_orders(session, customer_id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return orders


@router.get("/{customer_id}/tickets", response_model=list[CustomerTicketResponse])
async def read_customer_tickets(
    customer_id: int,
    session: AsyncSession = Depends(get_db),
) -> list[CustomerTicketResponse]:
    customer, tickets = await get_customer_tickets(session, customer_id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return tickets