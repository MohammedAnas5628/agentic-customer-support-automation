from dataclasses import dataclass

from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from backend.app.core.config import settings


EMBEDDING_MODEL = "models/gemini-embedding-001"


@dataclass(frozen=True)
class EmbeddedDocument:
    """A chunk and its embedding, retaining the chunk's metadata."""

    document: Document
    embedding: list[float]


def embed_documents(documents: list[Document]) -> list[EmbeddedDocument]:
    """Generate Gemini embeddings for document content without storing them."""
    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=settings.gemini_api_key,
    )
    vectors = embeddings.embed_documents(
        [document.page_content for document in documents]
    )
    return [
        EmbeddedDocument(document=document, embedding=vector)
        for document, vector in zip(documents, vectors, strict=True)
    ]


def embed_query(query: str) -> list[float]:
    """Generate one query vector with the same model as stored documents."""
    if not query.strip():
        raise ValueError("Cannot embed an empty query.")

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=settings.gemini_api_key,
    )
    vector = embeddings.embed_query(query)
    if len(vector) != 3072:
        raise ValueError(
            f"Query embedding dimension mismatch: expected 3072, got {len(vector)}."
        )
    return vector