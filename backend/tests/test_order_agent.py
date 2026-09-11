from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from backend.app.agents import order_agent
from backend.app.tools import order_tools


class FakeSession:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return False


@pytest.mark.asyncio
async def test_get_order_tool_returns_validated_order(monkeypatch):
    monkeypatch.setattr(
        order_tools,
        "get_order_by_number",
        AsyncMock(return_value=SimpleNamespace(order_number="EM-123", status="processing")),
    )

    result = await order_tools.get_order_tool(FakeSession(), "EM-123")

    assert result.success is True
    assert result.tool == "get_order"
    assert "processing" in result.message


@pytest.mark.asyncio
async def test_refund_tool_handles_missing_refund(monkeypatch):
    monkeypatch.setattr(
        order_tools,
        "get_order_with_refund",
        AsyncMock(return_value=SimpleNamespace(order_number="EM-123", payment=None)),
    )

    result = await order_tools.get_refund_tool(FakeSession(), "EM-123")

    assert result.success is True
    assert "No refund" in result.message


@pytest.mark.asyncio
async def test_cancel_tool_accepts_only_eligible_status(monkeypatch):
    monkeypatch.setattr(
        order_tools,
        "cancel_order_service",
        AsyncMock(
            return_value=(
                SimpleNamespace(order_number="EM-123", status="cancelled"),
                "processing",
            )
        ),
    )

    result = await order_tools.cancel_order_tool(FakeSession(), "EM-123")

    assert result.success is True
    assert result.data["new_status"] == "cancelled"


@pytest.mark.asyncio
async def test_cancel_tool_rejects_ineligible_status(monkeypatch):
    monkeypatch.setattr(
        order_tools,
        "cancel_order_service",
        AsyncMock(
            return_value=(SimpleNamespace(order_number="EM-123", status="shipped"), "shipped")
        ),
    )

    result = await order_tools.cancel_order_tool(FakeSession(), "EM-123")

    assert result.success is False
    assert "cannot cancel" in result.message


@pytest.mark.asyncio
async def test_order_agent_selects_tool_and_rejects_invalid_argument(monkeypatch):
    get_order = AsyncMock(
        return_value=order_tools.OrderToolResult(True, "get_order", "Order found.")
    )
    monkeypatch.setattr(order_agent, "get_order_tool", get_order)
    monkeypatch.setattr(order_agent, "AsyncSessionLocal", FakeSession)

    result = await order_agent.run_order_agent("Where is order EM-123?")

    assert result.tool == "get_order"
    get_order.assert_awaited_once()
    invalid = await order_agent.run_order_agent("Where is my order?")
    assert invalid.tool == "order_agent"
    assert not invalid.success