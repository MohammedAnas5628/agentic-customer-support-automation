from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.schemas.refund import RefundResponse
from backend.app.services.refund_service import get_order_with_refund


router = APIRouter(prefix="/api/orders", tags=["refunds"])


@router.get("/{order_number}/refund", response_model=RefundResponse)
async def read_order_refund(
    order_number: str,
    session: AsyncSession = Depends(get_db),
) -> RefundResponse:
    order = await get_order_with_refund(session, order_number)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    payment = order.payment
    refund = payment.refunds[0] if payment and payment.refunds else None

    if refund is None:
        return RefundResponse(
            order_number=order.order_number,
            refund_status=None,
            refund_amount=None,
            refund_transaction_id=None,
            reason=None,
            processed_at=None,
            created_at=None,
            updated_at=None,
            payment_status=payment.payment_status if payment else None,
            payment_method=payment.payment_method if payment else None,
            message="No refund found for this order.",
        )

    return RefundResponse(
        order_number=order.order_number,
        refund_status=refund.refund_status,
        refund_amount=refund.amount,
        refund_transaction_id=refund.refund_transaction_id,
        reason=refund.reason,
        processed_at=refund.processed_at,
        created_at=refund.created_at,
        updated_at=refund.updated_at,
        payment_status=payment.payment_status if payment else None,
        payment_method=payment.payment_method if payment else None,
        message="Refund found for this order.",
    )