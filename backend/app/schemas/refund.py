from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class RefundResponse(BaseModel):
    order_number: str
    refund_status: str | None
    refund_amount: Decimal | None
    refund_transaction_id: str | None
    reason: str | None
    processed_at: datetime | None
    created_at: datetime | None
    updated_at: datetime | None
    payment_status: str | None
    payment_method: str | None
    message: str