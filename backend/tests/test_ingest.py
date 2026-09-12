from dataclasses import dataclass
from unittest.mock import AsyncMock

import pytest

from backend.app.rag import ingest
from backend.app.rag.document_loader import load_knowledge_base


@dataclass
class FakeEmbeddedDocument:
    document: object
    embedding: list[float]


def _fake_embeddings(chunks):
    return [
        FakeEmbeddedDocument(chunk, [0.0] * 384)
        for chunk in chunks
    ]


@pytest.mark.asyncio
async def test_ingestion_loads_15_documents_and_stores_145_chunks(monkeypatch):
    documents = load_knowledge_base()
    replace = AsyncMock(return_value=[object()] * 145)
    monkeypatch.setattr(ingest, "replace_embedded_documents", replace)
    monkeypatch.setattr(ingest, "embed_documents", _fake_embeddings)

    result = await ingest.ingest_knowledge_base(object())

    assert result.documents_processed == 15
    assert result.chunks_generated == 145
    assert result.records_stored == 145
    embedded = replace.call_args.args[1]
    assert len(embedded) == 145
    assert {item.document.metadata["source"] for item in embedded} == {
        document.metadata["source"] for document in documents
    }


@pytest.mark.asyncio
async def test_ingestion_replaces_existing_snapshot(monkeypatch):
    replace = AsyncMock(return_value=[object()] * 145)
    monkeypatch.setattr(ingest, "replace_embedded_documents", replace)
    monkeypatch.setattr(ingest, "embed_documents", _fake_embeddings)

    first = await ingest.ingest_knowledge_base(object())
    second = await ingest.ingest_knowledge_base(object())

    assert first.records_stored == second.records_stored == 145
    assert replace.await_count == 2


@pytest.mark.asyncio
async def test_embedding_failure_is_explicit_and_storage_is_not_called(monkeypatch):
    replace = AsyncMock()
    monkeypatch.setattr(ingest, "replace_embedded_documents", replace)

    def fail(_chunks):
        raise RuntimeError("429 RESOURCE_EXHAUSTED")

    monkeypatch.setattr(ingest, "embed_documents", fail)

    with pytest.raises(RuntimeError, match="embedding generation failed"):
        await ingest.ingest_knowledge_base(object())

    replace.assert_not_awaited()