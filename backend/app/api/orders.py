from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.core.security import get_current_user
from backend.app.models.customer import Customer
from backend.app.schemas.order import OrderCreate, OrderResponse
from backend.app.services.orders import create_order, get_order_by_number


router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_order(
    payload: OrderCreate,
    session: AsyncSession = Depends(get_db),
    current_user: Customer = Depends(get_current_user),
) -> OrderResponse:
    try:
        order = await create_order(
            session=session,
            customer_id=current_user.id,
            data=payload,
        )
        return order
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        )


@router.get(
    "/{order_number}",
    response_model=OrderResponse,
)
async def read_order(
    order_number: str,
    session: AsyncSession = Depends(get_db),
    current_user: Customer = Depends(get_current_user),
) -> OrderResponse:
    order = await get_order_by_number(session, order_number)
    if order is None or (current_user.role == "customer" and order.customer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return order