import asyncio
from dataclasses import dataclass
from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.rag_document_chunk import RagDocumentChunk
from backend.app.rag.embeddings import embed_query


DEFAULT_TOP_K = 5
DEFAULT_RELEVANCE_THRESHOLD = 0.55


@dataclass(frozen=True)
class RetrievedChunk:
    content: str
    source: str
    similarity: float


async def retrieve_chunks(
    session: AsyncSession,
    query: str,
    top_k: int = DEFAULT_TOP_K,
    relevance_threshold: float = DEFAULT_RELEVANCE_THRESHOLD,
    query_variants: Iterable[str] | None = None,
) -> list[RetrievedChunk]:
    """Retrieve relevant chunks using pgvector cosine distance."""
    if top_k < 1:
        raise ValueError("top_k must be at least 1.")
    if not 0 <= relevance_threshold <= 1:
        raise ValueError("relevance_threshold must be between 0 and 1.")

    variants = list(dict.fromkeys(query_variants or [query]))
    best_matches: dict[tuple[str, str], RetrievedChunk] = {}
    for variant in variants:
        query_vector = await asyncio.to_thread(embed_query, variant)
        distance = RagDocumentChunk.embedding.cosine_distance(query_vector).label("distance")
        statement = select(RagDocumentChunk, distance).order_by(distance).limit(top_k)
        result = await session.execute(statement)
        for document, raw_distance in result.all():
            similarity = 1.0 - float(raw_distance)
            if similarity < relevance_threshold:
                continue
            key = (document.source, document.content)
            current = best_matches.get(key)
            if current is None or similarity > current.similarity:
                best_matches[key] = RetrievedChunk(document.content, document.source, similarity)
    return sorted(best_matches.values(), key=lambda chunk: chunk.similarity, reverse=True)[:top_k]