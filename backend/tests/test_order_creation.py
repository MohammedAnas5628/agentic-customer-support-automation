from types import SimpleNamespace
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError

from backend.app.api.orders import create_new_order
from backend.app.schemas.order import OrderCreate, OrderItemCreate


class FakeSession:
    def __init__(self):
        pass


def test_protected_order_create_requires_authentication():
    app = FastAPI()
    app.add_api_route("/api/orders", create_new_order, methods=["POST"])

    client = TestClient(app)
    response = client.post("/api/orders", json={"items": [{"product_id": 22, "quantity": 1}]})

    assert response.status_code == 401


def test_order_create_schema_validation():
    # Valid payload
    payload = OrderCreate(
        items=[OrderItemCreate(product_id=22, quantity=2)],
        shipping_address="Test Address, Hyderabad",
        payment_method="UPI",
    )
    assert len(payload.items) == 1
    assert payload.items[0].quantity == 2

    # Empty items list should raise validation error
    with pytest.raises(ValidationError):
        OrderCreate(items=[])

    # Zero or negative quantity should raise validation error
    with pytest.raises(ValidationError):
        OrderItemCreate(product_id=22, quantity=0)
