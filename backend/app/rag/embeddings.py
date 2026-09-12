from dataclasses import dataclass
from functools import lru_cache

from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer


EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIMENSION = 384


@dataclass(frozen=True)
class EmbeddedDocument:
    """A chunk and its embedding, retaining the chunk's metadata."""

    document: Document
    embedding: list[float]


@lru_cache(maxsize=1)
def _get_model() -> SentenceTransformer:
    """Load and cache the local model, downloading it on first use."""
    return SentenceTransformer(EMBEDDING_MODEL)


def _encode(texts: list[str]) -> list[list[float]]:
    vectors = _get_model().encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return [vector.tolist() if hasattr(vector, "tolist") else list(vector) for vector in vectors]


def embed_documents(documents: list[Document]) -> list[EmbeddedDocument]:
    """Generate local BGE embeddings for document content without storing them."""
    vectors = _encode([document.page_content for document in documents])
    if any(len(vector) != EMBEDDING_DIMENSION for vector in vectors):
        raise ValueError(f"Document embedding dimension mismatch: expected {EMBEDDING_DIMENSION}.")
    return [
        EmbeddedDocument(document=document, embedding=vector)
        for document, vector in zip(documents, vectors, strict=True)
    ]


def embed_query(query: str) -> list[float]:
    """Generate one query vector with the same model as stored documents."""
    if not query.strip():
        raise ValueError("Cannot embed an empty query.")

    vector = _encode([query])[0]
    if len(vector) != EMBEDDING_DIMENSION:
        raise ValueError(
            f"Query embedding dimension mismatch: expected {EMBEDDING_DIMENSION}, got {len(vector)}."
        )
    return vector