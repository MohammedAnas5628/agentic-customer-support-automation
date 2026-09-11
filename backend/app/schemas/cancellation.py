from pydantic import BaseModel


class OrderCancellationResponse(BaseModel):
    order_number: str
    previous_status: str
    new_status: str
    message: str