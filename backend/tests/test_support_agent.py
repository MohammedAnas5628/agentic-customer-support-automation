from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from backend.app.agents import support_agent
from backend.app.tools import ticket_tools
from backend.app.tools.ticket_tools import TicketToolResult


class FakeSession:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return False


@pytest.mark.asyncio
async def test_create_ticket_tool_validates_references_and_creates(monkeypatch):
    monkeypatch.setattr(
        ticket_tools,
        "create_ticket_service",
        AsyncMock(return_value=SimpleNamespace(ticket_number="TKT10001", status="open")),
    )

    result = await ticket_tools.create_ticket_tool(
        FakeSession(), customer_id=1, subject="Damaged product", description="The screen is cracked."
    )

    assert result.success is True
    assert result.data["ticket_number"] == "TKT10001"


@pytest.mark.asyncio
async def test_get_ticket_tool_handles_unknown_ticket(monkeypatch):
    monkeypatch.setattr(ticket_tools, "get_ticket_by_number", AsyncMock(return_value=None))

    result = await ticket_tools.get_ticket_tool(FakeSession(), "TKT99999")

    assert result.success is False
    assert "find" in result.message


@pytest.mark.asyncio
async def test_update_ticket_tool_validates_allowed_changes(monkeypatch):
    update = AsyncMock(return_value=SimpleNamespace(ticket_number="TKT10001", status="resolved", priority="high"))
    monkeypatch.setattr(ticket_tools, "update_ticket_service", update)

    result = await ticket_tools.update_ticket_tool(
        FakeSession(), "TKT10001", {"status": "resolved", "priority": "high"}
    )
    invalid = await ticket_tools.update_ticket_tool(
        FakeSession(), "TKT10001", {"assigned_to": "admin"}
    )

    assert result.success is True
    assert invalid.success is False
    update.assert_awaited_once()


@pytest.mark.asyncio
async def test_support_agent_selects_get_tool(monkeypatch):
    get_tool = AsyncMock(return_value=TicketToolResult(True, "get_ticket", "Ticket is open."))
    monkeypatch.setattr(support_agent, "get_ticket_tool", get_tool)
    monkeypatch.setattr(support_agent, "AsyncSessionLocal", FakeSession)

    result = await support_agent.run_support_agent("What's the status of TKT10001?")

    assert result.tool == "get_ticket"
    get_tool.assert_awaited_once()


@pytest.mark.asyncio
async def test_support_agent_does_not_invent_customer_for_creation():
    result = await support_agent.run_support_agent("Create a ticket for my damaged product")

    assert result.success is False
    assert result.tool == "support_agent"