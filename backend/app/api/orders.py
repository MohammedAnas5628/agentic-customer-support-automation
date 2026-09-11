from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.schemas.order import OrderResponse
from backend.app.services.orders import get_order_by_number


router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.get(
    "/{order_number}",
    response_model=OrderResponse,
)
async def read_order(
    order_number: str,
    session: AsyncSession = Depends(get_db),
) -> OrderResponse:
    order = await get_order_by_number(session, order_number)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return order