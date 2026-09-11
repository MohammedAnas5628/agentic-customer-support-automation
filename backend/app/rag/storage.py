from collections.abc import Sequence

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.rag_document_chunk import RagDocumentChunk
from backend.app.rag.embeddings import EmbeddedDocument


async def store_embedded_documents(
    session: AsyncSession,
    embedded_documents: Sequence[EmbeddedDocument],
) -> list[RagDocumentChunk]:
    """Store embedded chunks in the dedicated RAG table."""
    records = [
        RagDocumentChunk(
            content=embedded.document.page_content,
            source=embedded.document.metadata["source"],
            embedding=embedded.embedding,
        )
        for embedded in embedded_documents
    ]
    session.add_all(records)
    await session.flush()
    return records


async def replace_embedded_documents(
    session: AsyncSession,
    embedded_documents: Sequence[EmbeddedDocument],
) -> list[RagDocumentChunk]:
    """Replace the full knowledge-base snapshot in the current transaction."""
    await session.execute(delete(RagDocumentChunk))
    return await store_embedded_documents(session, embedded_documents)