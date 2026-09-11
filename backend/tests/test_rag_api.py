from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.rag.generation import GroundedAnswer
from backend.app.api import rag


def test_rag_query_api_returns_answer_sources_and_status(monkeypatch):
    async def fake_knowledge_agent(_query):
        return GroundedAnswer(
            "The return policy is described in the knowledge base.",
            [{"source": "returns_and_refunds.md", "score": 0.91}],
            [],
            "answered",
        )

    monkeypatch.setattr(rag, "run_knowledge_agent", fake_knowledge_agent)
    response = TestClient(app).post(
        "/api/rag/query",
        json={"query": "What is the return policy?"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "The return policy is described in the knowledge base.",
        "sources": [{"source": "returns_and_refunds.md", "score": 0.91}],
        "status": "answered",
    }


def test_rag_query_api_hides_internal_failures(monkeypatch):
    async def failing_knowledge_agent(_query):
        raise RuntimeError("internal database details")

    monkeypatch.setattr(rag, "run_knowledge_agent", failing_knowledge_agent)
    response = TestClient(app).post("/api/rag/query", json={"query": "Return policy?"})

    assert response.status_code == 200
    assert response.json()["status"] == "error"
    assert response.json()["sources"] == []
    assert "internal database details" not in response.text