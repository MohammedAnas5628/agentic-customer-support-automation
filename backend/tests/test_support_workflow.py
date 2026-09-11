import pytest

from backend.app.rag.generation import GroundedAnswer
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