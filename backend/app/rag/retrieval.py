import asyncio
from dataclasses import dataclass
from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.rag_document_chunk import RagDocumentChunk
from backend.app.rag.embeddings import embed_query


import re

STOP_WORDS = {
    "what", "when", "where", "which", "who", "whom", "whose", "why", "how",
    "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did",
    "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
    "of", "at", "by", "for", "with", "about", "against", "between", "into", "through",
    "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out",
    "on", "off", "over", "under", "again", "further", "then", "once",
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "yourselves", "it", "its", "can", "could", "should", "would",
}


def _lexical_overlap(query_text: str, doc_text: str) -> float:
    """Calculate token overlap between query terms and chunk content for hybrid scoring."""
    words = [w for w in re.findall(r"\w+", query_text.lower()) if len(w) > 2 and w not in STOP_WORDS]
    if not words:
        return 0.0
    doc_words = set(re.findall(r"\w+", doc_text.lower()))
    match_count = sum(1 for w in set(words) if w in doc_words)
    return match_count / len(set(words))


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
    """Retrieve relevant chunks using hybrid vector search and lexical reranking."""
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
        keyword_score = _lexical_overlap(query, chunk.content)
        # Hybrid score: vector similarity (65%) + exact keyword match (15%) + multi-query coverage (12%) + rank position (8%)
        return 0.65 * similarity + 0.15 * keyword_score + 0.12 * coverage_score + 0.08 * rank_score

    return sorted(best_matches.values(), key=rerank_score, reverse=True)[:top_k]