from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TicketCustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    phone: str | None


class TicketOrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_number: str


class TicketResponse(BaseModel):
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
    customer: TicketCustomerResponse
    order: TicketOrderResponse | None


class TicketCreate(BaseModel):
    customer_id: int
    order_number: str | None = None
    subject: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=10000, pattern=r"^[^\x00-\x08\x0b\x0c\x0e-\x1f\x7f]+$")
    status: str = Field(default="open", min_length=1, max_length=30)
    priority: str = Field(default="normal", min_length=1, max_length=20)


class TicketUpdate(BaseModel):
    subject: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1, max_length=10000, pattern=r"^[^\x00-\x08\x0b\x0c\x0e-\x1f\x7f]+$")
    status: str | None = Field(default=None, min_length=1, max_length=30)
    priority: str | None = Field(default=None, min_length=1, max_length=20)