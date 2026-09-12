from types import SimpleNamespace

import pytest

from backend.app.agents import knowledge_agent
from backend.app.models.rag_document_chunk import RagDocumentChunk
from backend.app.rag import generation, retrieval
from backend.app.rag.generation import NO_CONTEXT_RESPONSE
from backend.app.rag.retrieval import RetrievedChunk


class FakeResult:
    def __init__(self, rows):
        self.rows = rows

    def all(self):
        return self.rows


class FakeSession:
    def __init__(self, rows):
        self.rows = rows
        self.statement = None

    async def execute(self, statement):
        self.statement = statement
        return FakeResult(self.rows)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return False


def _chunk(source: str, content: str) -> RagDocumentChunk:
    return RagDocumentChunk(content=content, source=source, embedding=[0.0] * 384)


def test_policy_query_variants_cover_natural_paraphrases():
    from backend.app.agents.knowledge_agent import query_variants

    variants = query_variants("How many days do I have to return something?")

    assert variants[0].startswith("How many days")
    assert "return policy product return eligibility" in variants


@pytest.mark.asyncio
async def test_retrieval_embeds_query_orders_results_and_respects_top_k(monkeypatch):
    called = []
    monkeypatch.setattr(
        retrieval,
        "embed_query",
        lambda query: called.append(query) or [0.1] * 384,
    )
    session = FakeSession(
        [
            (_chunk("returns_and_refunds.md", "Return details"), 0.1),
            (_chunk("warranty.md", "Warranty details"), 0.2),
        ]
    )

    results = await retrieval.retrieve_chunks(
        session,
        "What is the return policy?",
        top_k=2,
        relevance_threshold=0.7,
    )

    assert called == ["What is the return policy?"]
    assert [result.source for result in results] == [
        "returns_and_refunds.md",
        "warranty.md",
    ]
    assert [result.similarity for result in results] == [0.9, 0.8]
    assert session.statement._limit_clause.value == 2


@pytest.mark.asyncio
async def test_retrieval_filters_weak_results(monkeypatch):
    monkeypatch.setattr(retrieval, "embed_query", lambda _query: [0.1] * 384)
    session = FakeSession([(_chunk("general_faq.md", "Weak match"), 0.7)])

    results = await retrieval.retrieve_chunks(
        session,
        "Unrelated question",
        relevance_threshold=0.5,
    )

    assert results == []


class FakeChatModel:
    def __init__(self, content="Grounded answer"):
        self.content = content
        self.messages = None

    async def ainvoke(self, messages):
        self.messages = messages
        return SimpleNamespace(content=self.content)


@pytest.mark.asyncio
async def test_generation_passes_context_and_sources_to_customer_answer():
    model = FakeChatModel()
    chunks = [RetrievedChunk("Delivery takes 3-5 days.", "shipping_and_delivery.md", 0.88)]

    result = await generation.generate_grounded_answer("How long is delivery?", chunks, model)

    assert result.answer == "Grounded answer"
    assert result.sources == [{"source": "shipping_and_delivery.md", "score": 0.88}]
    assert result.status == "answered"
    assert "ONLY the supplied ElectroMart knowledge context" in model.messages[0].content
    assert "Delivery takes 3-5 days." in model.messages[1].content


@pytest.mark.asyncio
async def test_generation_does_not_call_llm_without_context():
    model = FakeChatModel()

    result = await generation.generate_grounded_answer("Unknown", [], model)

    assert result.answer == NO_CONTEXT_RESPONSE
    assert result.status == "no_context"
    assert model.messages is None


@pytest.mark.asyncio
async def test_knowledge_agent_connects_retrieval_to_generation(monkeypatch):
    chunks = [RetrievedChunk("Warranty is two years.", "warranty.md", 0.91)]
    expected = generation.GroundedAnswer(
        "Warranty is two years.",
        [{"source": "warranty.md", "score": 0.91}],
        [{"content": "Warranty is two years.", "source": "warranty.md", "similarity": 0.91}],
        "answered",
    )
    monkeypatch.setattr(knowledge_agent, "AsyncSessionLocal", lambda: FakeSession([]))
    monkeypatch.setattr(knowledge_agent, "retrieve_chunks", _async_return(chunks))
    monkeypatch.setattr(knowledge_agent, "generate_grounded_answer", _async_return(expected))

    result = await knowledge_agent.run_knowledge_agent("How long is the warranty?")

    assert result == expected


def _async_return(value):
    async def return_value(*_args, **_kwargs):
        return value

    return return_value