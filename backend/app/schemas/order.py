from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CustomerOrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    phone: str | None


class ProductOrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sku: str
    name: str
    brand: str
    category: str
    price: Decimal


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    product: ProductOrderResponse


class RefundResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    refund_status: str
    amount: Decimal
    refund_transaction_id: str | None
    reason: str | None
    processed_at: datetime | None


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    payment_method: str
    payment_status: str
    transaction_id: str | None
    amount: Decimal
    paid_at: datetime | None
    refunds: list[RefundResponse]


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_number: str
    status: str
    subtotal: Decimal
    shipping_fee: Decimal
    discount: Decimal
    total_amount: Decimal
    shipping_address: str
    tracking_number: str | None
    created_at: datetime
    updated_at: datetime
    customer: CustomerOrderResponse
    items: list[OrderItemResponse]
    payment: PaymentResponse | None