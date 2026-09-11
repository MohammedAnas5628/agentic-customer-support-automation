import pytest

from backend.app.rag.generation import GroundedAnswer
from backend.app.tools.order_tools import OrderToolResult
from backend.app.tools.ticket_tools import TicketToolResult
from backend.app.tools.escalation_tools import EscalationResult
from backend.app.workflows import support_workflow
from backend.app.workflows.support_workflow import (
    build_support_graph,
    run_support_workflow,
)


@pytest.fixture
def mock_knowledge_agent(monkeypatch):
    async def run(_question):
        return GroundedAnswer(
            "Grounded answer",
            [{"source": "general_faq.md", "score": 0.9}],
            [{"content": "Grounded context", "source": "general_faq.md", "similarity": 0.9}],
            "answered",
        )

    monkeypatch.setattr(support_workflow, "run_knowledge_agent", run)


@pytest.mark.parametrize(
    ("intent", "agent"),
    [
        ("knowledge", "knowledge"),
        ("order", "order"),
        ("support", "support"),
        ("escalation", "escalation"),
    ],
)
def test_routes_to_only_the_selected_agent(intent, agent, mock_knowledge_agent):
    result = run_support_workflow("A customer message", intent)

    assert result["user_message"] == "A customer message"
    assert result["intent"] == intent
    assert result["selected_agent"] == agent
    assert result["executed_nodes"] == ["router", agent]
    assert result["final_response"]


def test_unknown_intent_uses_safe_fallback():
    result = run_support_workflow("An unsupported request", "unknown")

    assert result["selected_agent"] == "fallback"
    assert result["executed_nodes"] == ["router", "fallback"]
    assert "not determine" in result["final_response"]


def test_graph_compiles():
    assert build_support_graph() is not None


@pytest.mark.asyncio
async def test_order_route_reaches_order_agent(monkeypatch):
    async def run_order_agent(_message):
        return OrderToolResult(True, "get_order", "Order EM-123 is currently processing.")

    monkeypatch.setattr(support_workflow, "run_order_agent", run_order_agent)
    result = await support_workflow.run_support_workflow_async(
        "Where is order EM-123?",
        "order",
    )

    assert result["selected_agent"] == "order"
    assert result["order_tool"] == "get_order"
    assert result["executed_nodes"] == ["router", "order"]
    assert "processing" in result["final_response"]


@pytest.mark.asyncio
async def test_support_route_reaches_support_agent(monkeypatch):
    async def run_support_agent(_message):
        return TicketToolResult(True, "create_ticket", "Support ticket TKT10001 was created.")

    monkeypatch.setattr(support_workflow, "run_support_agent", run_support_agent)
    result = await support_workflow.run_support_workflow_async(
        "I received a damaged product",
        "support",
    )

    assert result["selected_agent"] == "support"
    assert result["support_tool"] == "create_ticket"
    assert result["executed_nodes"] == ["router", "support"]
    assert "TKT10001" in result["final_response"]


@pytest.mark.asyncio
async def test_escalation_route_reaches_escalation_agent(monkeypatch):
    async def run_escalation_agent(_message, **_kwargs):
        return EscalationResult(
            True,
            "Your issue has been escalated under ticket TKT10001.",
            "human_requested",
            "normal",
            "TKT10001",
        )

    monkeypatch.setattr(support_workflow, "run_escalation_agent", run_escalation_agent)
    result = await support_workflow.run_support_workflow_async(
        "I want to speak to a human, customer_id=1",
        "escalation",
    )

    assert result["selected_agent"] == "escalation"
    assert result["escalation_status"] == "pending"
    assert result["handoff_reference"] == "TKT10001"
    assert result["executed_nodes"] == ["router", "escalation"]