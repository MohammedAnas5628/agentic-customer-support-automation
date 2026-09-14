from types import SimpleNamespace

import pytest

from backend.app.services import conversation_memory


class FakeModel:
    async def ainvoke(self, _messages):
        return SimpleNamespace(content="Customer is tracking order EM-100; return policy question remains open.")


class FakeSession:
    def __init__(self, messages):
        self.messages = messages
        self.commits = 0

    async def scalars(self, _statement):
        return self.messages

    async def commit(self):
        self.commits += 1


@pytest.mark.asyncio
async def test_compaction_summarizes_older_turns_and_keeps_raw_messages(monkeypatch):
    monkeypatch.setattr(conversation_memory.settings, "memory_compaction_message_threshold", 24)
    monkeypatch.setattr(conversation_memory.settings, "memory_recent_message_limit", 12)
    conversation = SimpleNamespace(
        id=4,
        memory_summary=None,
        summary_through_message_id=None,
    )
    messages = [
        SimpleNamespace(id=index, sender_type="customer" if index % 2 else "assistant", content=f"turn {index}")
        for index in range(1, 25)
    ]
    session = FakeSession(messages)

    compacted = await conversation_memory.compact_conversation(
        session, conversation, llm=FakeModel()
    )

    assert compacted is True
    assert conversation.memory_summary.startswith("Customer is tracking")
    assert conversation.summary_through_message_id == 12
    assert len(session.messages) == 24
    assert session.commits == 1
