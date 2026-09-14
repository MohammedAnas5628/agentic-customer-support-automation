import asyncio
from dataclasses import dataclass
from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.rag_document_chunk import RagDocumentChunk
from backend.app.rag.embeddings import embed_query


DEFAULT_TOP_K = 5
DEFAULT_RELEVANCE_THRESHOLD = 0.55
DEFAULT_CANDIDATE_MULTIPLIER = 3


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
    candidate_multiplier: int = DEFAULT_CANDIDATE_MULTIPLIER,
) -> list[RetrievedChunk]:
    """Retrieve relevant chunks using pgvector cosine distance."""
    if top_k < 1:
        raise ValueError("top_k must be at least 1.")
    if not 0 <= relevance_threshold <= 1:
        raise ValueError("relevance_threshold must be between 0 and 1.")
    if candidate_multiplier < 1:
        raise ValueError("candidate_multiplier must be at least 1.")

    variants = list(dict.fromkeys(query_variants or [query]))
    candidate_limit = top_k * candidate_multiplier
    best_matches: dict[tuple[str, str], RetrievedChunk] = {}
    ranking_data: dict[tuple[str, str], tuple[float, int, int]] = {}
    for variant in variants:
        query_vector = await asyncio.to_thread(embed_query, variant)
        distance = RagDocumentChunk.embedding.cosine_distance(query_vector).label("distance")
        statement = select(RagDocumentChunk, distance).order_by(distance).limit(candidate_limit)
        result = await session.execute(statement)
        for rank, (document, raw_distance) in enumerate(result.all(), start=1):
            similarity = 1.0 - float(raw_distance)
            if similarity < relevance_threshold:
                continue
            key = (document.source, document.content)
            current = best_matches.get(key)
            if current is None or similarity > current.similarity:
                best_matches[key] = RetrievedChunk(document.content, document.source, similarity)
            previous_similarity, previous_rank, variant_count = ranking_data.get(
                key, (0.0, rank, 0)
            )
            ranking_data[key] = (
                max(previous_similarity, similarity),
                min(previous_rank, rank),
                variant_count + 1,
            )

    def rerank_score(chunk: RetrievedChunk) -> float:
        similarity, best_rank, variant_count = ranking_data[(chunk.source, chunk.content)]
        rank_score = 1.0 / (60 + best_rank)
        coverage_score = variant_count / len(variants)
        return 0.75 * similarity + 0.15 * coverage_score + 0.10 * rank_score

    return sorted(best_matches.values(), key=rerank_score, reverse=True)[:top_k]