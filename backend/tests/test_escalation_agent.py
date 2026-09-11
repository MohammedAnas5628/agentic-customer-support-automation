from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from backend.app.agents import escalation_agent
from backend.app.tools import escalation_tools


class FakeSession:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return False


@pytest.mark.asyncio
async def test_handoff_creates_pending_ticket(monkeypatch):
    monkeypatch.setattr(
        escalation_tools,
        "create_ticket_tool",
        AsyncMock(
            return_value=escalation_tools.TicketToolResult(
                True, "create_ticket", "created", {"ticket_number": "TKT10001"}
            )
        ),
    )

    result = await escalation_tools.escalate_to_human(
        FakeSession(),
        reason="human_requested",
        summary="Customer requested a human.",
        customer_id=1,
    )

    assert result.success is True
    assert result.ticket_number == "TKT10001"
    assert result.priority == "normal"


@pytest.mark.asyncio
async def test_handoff_updates_existing_ticket_with_urgent_priority(monkeypatch):
    update = AsyncMock(
        return_value=escalation_tools.TicketToolResult(True, "update_ticket", "updated")
    )
    monkeypatch.setattr(escalation_tools, "update_ticket_tool", update)

    result = await escalation_tools.escalate_to_human(
        FakeSession(),
        reason="security_risk",
        summary="Customer reports unauthorized account access.",
        ticket_number="TKT10001",
    )

    assert result.success is True
    assert result.priority == "urgent"
    update.assert_awaited_once()
    assert update.call_args.args[2]["status"] == "pending"


@pytest.mark.asyncio
async def test_invalid_handoff_input_is_rejected():
    result = await escalation_tools.escalate_to_human(
        FakeSession(), reason="made_up_reason", summary="Something happened."
    )

    assert result.success is False
    assert "validate" in result.message


@pytest.mark.asyncio
async def test_no_context_escalation_does_not_invent_customer(monkeypatch):
    monkeypatch.setattr(escalation_agent, "AsyncSessionLocal", FakeSession)
    handoff = AsyncMock(
        return_value=escalation_tools.EscalationResult(
            False, "A valid customer reference is required.", "no_context", "normal"
        )
    )
    monkeypatch.setattr(escalation_agent, "escalate_to_human", handoff)

    result = await escalation_agent.run_escalation_agent(
        "The knowledge base could not answer this question.", rag_status="no_context"
    )

    assert result.success is False
    assert result.reason == "no_context"
    assert handoff.call_args.kwargs["customer_id"] is None