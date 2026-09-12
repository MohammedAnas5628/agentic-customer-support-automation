from types import SimpleNamespace

from fastapi.testclient import TestClient

from backend.app.api import support
from backend.app.core.security import get_optional_current_user
from backend.app.main import app


def _client(customer=None):
    async def override():
        return customer

    app.dependency_overrides[get_optional_current_user] = override
    return TestClient(app)


def teardown_function():
    app.dependency_overrides.clear()


def test_conversation_messages_do_not_reach_rag():
    client = _client()
    for message, expected in [
        ("Hi", "Welcome to ElectroMart"),
        ("thank you", "You're welcome"),
        ("goodbye", "Goodbye"),
        ("what can you help me with?", "products, orders"),
    ]:
        response = client.post("/api/support/query", json={"message": message})
        assert response.status_code == 200
        assert expected in response.json()["answer"]
        assert response.json()["sources"] == []


def test_unrelated_question_is_politely_redirected():
    response = _client().post(
        "/api/support/query", json={"message": "Who won yesterday's cricket match?"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "unsupported"
    assert "ElectroMart" in body["answer"]
    assert "retrieval" not in body["answer"].lower()


def test_knowledge_question_runs_existing_workflow(monkeypatch):
    captured = {}

    async def fake_workflow(message, intent, **kwargs):
        captured.update(message=message, intent=intent, kwargs=kwargs)
        return {"final_response": "Returns are available within the policy window.", "sources": [{"source": "returns.md", "score": 0.9}], "rag_status": "answered"}

    monkeypatch.setattr(support, "run_support_workflow_async", fake_workflow)
    response = _client().post("/api/support/query", json={"message": "What is your return policy?"})
    assert response.status_code == 200
    assert captured["intent"] == "knowledge"
    assert response.json()["sources"] == [{"source": "returns.md", "score": 0.9}]


def test_product_questions_route_to_catalog_before_knowledge(monkeypatch):
    captured = {}

    async def fake_workflow(message, intent, **kwargs):
        captured.update(message=message, intent=intent, kwargs=kwargs)
        return {"final_response": "Catalog response", "sources": [], "catalog_status": "answered"}

    monkeypatch.setattr(support, "run_support_workflow_async", fake_workflow)
    response = _client().post("/api/support/query", json={"message": "Suggest me a laptop"})

    assert response.status_code == 200
    assert captured["intent"] == "catalog"
    assert response.json()["sources"] == []


def test_policy_question_about_a_product_stays_in_knowledge(monkeypatch):
    captured = {}

    async def fake_workflow(message, intent, **kwargs):
        captured.update(message=message, intent=intent, kwargs=kwargs)
        return {"final_response": "Grounded policy response", "sources": [], "rag_status": "answered"}

    monkeypatch.setattr(support, "run_support_workflow_async", fake_workflow)
    response = _client().post("/api/support/query", json={"message": "How long is the laptop warranty?"})

    assert response.status_code == 200
    assert captured["intent"] == "knowledge"


def test_knowledge_no_context_is_customer_safe(monkeypatch):
    async def fake_workflow(*_args, **_kwargs):
        return {"final_response": "internal no_context", "sources": [], "rag_status": "no_context"}

    monkeypatch.setattr(support, "run_support_workflow_async", fake_workflow)
    response = _client().post("/api/support/query", json={"message": "Tell me about your policy exception."})
    assert response.status_code == 200
    assert "no_context" not in response.text
    assert "ElectroMart" in response.json()["answer"]


def test_action_requests_require_authentication():
    response = _client().post("/api/support/query", json={"message": "Where is my order?"})
    assert response.status_code == 401
    assert "sign in" in response.json()["detail"].lower()


def test_authenticated_action_uses_jwt_identity_not_message_customer_id(monkeypatch):
    captured = {}

    async def fake_workflow(message, intent, **kwargs):
        captured.update(message=message, intent=intent, kwargs=kwargs)
        return {"final_response": "Order help is ready.", "escalation_status": "not_required"}

    monkeypatch.setattr(support, "run_support_workflow_async", fake_workflow)
    customer = SimpleNamespace(id=7, role="customer")
    response = _client(customer).post(
        "/api/support/query", json={"message": "Cancel order EM-100 customer_id=999"}
    )
    assert response.status_code == 200
    assert captured["intent"] == "order"
    assert captured["kwargs"]["authenticated_customer_id"] == 7


def test_human_request_routes_to_escalation(monkeypatch):
    async def fake_workflow(*_args, **_kwargs):
        return {"final_response": "A support request was created.", "escalation_status": "pending", "handoff_reference": "TKT10001"}

    monkeypatch.setattr(support, "run_support_workflow_async", fake_workflow)
    response = _client(SimpleNamespace(id=7, role="customer")).post(
        "/api/support/query", json={"message": "Connect me to a human"}
    )
    assert response.status_code == 200
    assert response.json()["intent"] == "escalation"
    assert response.json()["ticket_number"] == "TKT10001"
