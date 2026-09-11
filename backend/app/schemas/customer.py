from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    phone: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CustomerTicketOrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_number: str
    status: str


class CustomerTicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ticket_number: str
    subject: str
    description: str
    status: str
    priority: str
    assigned_to: str | None
    created_at: datetime
    updated_at: datetime
    order: CustomerTicketOrderResponse | None
