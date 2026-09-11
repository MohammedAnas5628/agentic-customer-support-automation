from types import SimpleNamespace

import jwt
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.auth import login
from backend.app.api.orders import read_order
from backend.app.core import security
from backend.app.core.config import settings


class FakeSession:
    def __init__(self, customer=None):
        self.customer = customer

    async def execute(self, _statement):
        return SimpleNamespace(scalar_one_or_none=lambda: self.customer)

    async def get(self, _model, _customer_id):
        return self.customer


@pytest.mark.asyncio
async def test_successful_authentication_and_jwt(monkeypatch):
    customer = SimpleNamespace(
        id=7,
        email="customer@example.com",
        password_hash=security.hash_password("correct-password"),
        is_active=True,
        role="customer",
    )
    monkeypatch.setattr(settings, "jwt_secret", "test-only-secret-32-bytes-long-key")
    authenticated = await security.authenticate_customer(
        FakeSession(customer), "customer@example.com", "correct-password"
    )

    token = security.create_access_token(authenticated)
    payload = jwt.decode(
        token,
        "test-only-secret-32-bytes-long-key",
        algorithms=["HS256"],
    )
    assert authenticated.id == 7
    assert payload["sub"] == "7"
    assert payload["role"] == "customer"


@pytest.mark.asyncio
async def test_invalid_credentials_are_rejected():
    customer = SimpleNamespace(
        id=7,
        email="customer@example.com",
        password_hash=security.hash_password("correct-password"),
        is_active=True,
        role="customer",
    )

    assert await security.authenticate_customer(
        FakeSession(customer), "customer@example.com", "wrong-password"
    ) is None


def test_protected_order_endpoint_requires_authentication():
    app = FastAPI()
    app.add_api_route("/orders/{order_number}", read_order, methods=["GET"])

    response = TestClient(app).get("/orders/EM-123")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_customer_cannot_access_another_customers_order():
    customer = SimpleNamespace(id=1, role="customer")
    order = SimpleNamespace(customer_id=2)

    with pytest.raises(Exception) as caught:
        await read_order("EM-123", FakeSession(), customer)

    assert getattr(caught.value, "status_code", None) == 404