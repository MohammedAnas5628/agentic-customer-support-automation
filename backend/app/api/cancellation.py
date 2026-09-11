from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.schemas.cancellation import OrderCancellationResponse
from backend.app.services.order_cancellation import cancel_order


router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post(
    "/{order_number}/cancel",
    response_model=OrderCancellationResponse,
)
async def cancel_order_endpoint(
    order_number: str,
    session: AsyncSession = Depends(get_db),
) -> OrderCancellationResponse:
    order, previous_status = await cancel_order(session, order_number)
    if order is None or previous_status is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    if order.status == "cancelled" and previous_status in {"processing", "packed"}:
        message = "Order cancelled successfully."
    else:
        message = f"Order cannot be cancelled because its status is '{previous_status}'."

    return OrderCancellationResponse(
        order_number=order.order_number,
        previous_status=previous_status,
        new_status=order.status,
        message=message,
    )