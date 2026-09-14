from types import SimpleNamespace

from fastapi.testclient import TestClient

from backend.app.api import support
from backend.app.core.security import get_optional_current_user
from backend.app.db.database import get_db
from backend.app.main import app


class FakeSession:
    async def rollback(self):
        pass


def test_authenticated_support_request_loads_and_saves_memory(monkeypatch):
    customer = SimpleNamespace(id=7, role="customer")
    conversation = SimpleNamespace(id=42)
    captured = {}
    saved = {}

    async def fake_workflow(message, intent, **kwargs):
        captured.update(message=message, intent=intent, kwargs=kwargs)
        return {
            "final_response": "Your return window is 30 days.",
            "sources": [{"source": "returns.md", "score": 0.91}],
            "rag_status": "answered",
        }

    async def fake_get_or_create(_session, customer_id, conversation_id):
        assert customer_id == 7
        assert conversation_id == 42
        return conversation

    async def fake_load_history(_session, conversation_id):
        assert conversation_id == 42
        return [{"role": "user", "content": "I bought a laptop."}]

    async def fake_save_turn(_session, _conversation, user_message, assistant_message):
        saved.update(user_message=user_message, assistant_message=assistant_message)

    async def current_user():
        return customer

    async def db_session():
        yield FakeSession()

    monkeypatch.setattr(support, "run_support_workflow_async", fake_workflow)
    monkeypatch.setattr(support, "get_or_create_conversation", fake_get_or_create)
    monkeypatch.setattr(support, "load_recent_history", fake_load_history)
    monkeypatch.setattr(support, "save_turn", fake_save_turn)
    app.dependency_overrides[get_optional_current_user] = current_user
    app.dependency_overrides[get_db] = db_session

    try:
        response = TestClient(app).post(
            "/api/support/query",
            json={"message": "Can I return it?", "conversation_id": 42},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["conversation_id"] == 42
    assert captured["kwargs"]["conversation_history"] == [
        {"role": "user", "content": "I bought a laptop."}
    ]
    assert saved == {
        "user_message": "Can I return it?",
        "assistant_message": "Your return window is 30 days.",
    }
