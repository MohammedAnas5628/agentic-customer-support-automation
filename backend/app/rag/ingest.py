import asyncio
import logging
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import AsyncSessionLocal, engine
from backend.app.rag.document_chunker import chunk_documents
from backend.app.rag.document_loader import load_knowledge_base
from backend.app.rag.embeddings import (
    EMBEDDING_DIMENSION,
    EmbeddedDocument,
    embed_documents,
)
from backend.app.rag.storage import replace_embedded_documents


logger = logging.getLogger(__name__)
@dataclass(frozen=True)
class IngestionResult:
    documents_processed: int
    chunks_generated: int
    records_stored: int


def _validate_embeddings(embedded_documents: list[EmbeddedDocument]) -> None:
    invalid = [
        index
        for index, embedded in enumerate(embedded_documents)
        if len(embedded.embedding) != EMBEDDING_DIMENSION
    ]
    if invalid:
        raise ValueError(
            f"Embedding dimension mismatch at indexes {invalid}; "
            f"expected {EMBEDDING_DIMENSION}."
        )


async def ingest_knowledge_base(session: AsyncSession) -> IngestionResult:
    """Load, chunk, embed, and replace the persisted knowledge-base snapshot."""
    documents = load_knowledge_base()
    chunks = chunk_documents(documents)
    logger.info("Loaded %d documents and generated %d chunks", len(documents), len(chunks))

    try:
        embedded_documents = embed_documents(chunks)
    except Exception as exc:
        raise RuntimeError(
            "Local embedding generation failed; no records were stored. "
            "Check the model download and local environment."
        ) from exc

    if len(embedded_documents) != len(chunks):
        raise ValueError(
            f"Embedding count mismatch: received {len(embedded_documents)} "
            f"for {len(chunks)} chunks."
        )
    _validate_embeddings(embedded_documents)

    records = await replace_embedded_documents(session, embedded_documents)
    logger.info("Stored %d embedded chunks", len(records))
    return IngestionResult(len(documents), len(chunks), len(records))


async def run_ingestion() -> IngestionResult:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await ingest_knowledge_base(session)
    await engine.dispose()
    return result


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        result = asyncio.run(run_ingestion())
    except RuntimeError as exc:
        logger.error("Knowledge-base ingestion stopped: %s", exc)
        raise SystemExit(1)
    except Exception:
        logger.exception("Knowledge-base ingestion failed")
        raise SystemExit(1)

    print(f"Documents processed: {result.documents_processed}")
    print(f"Chunks generated: {result.chunks_generated}")
    print(f"Successful database inserts: {result.records_stored}")


if __name__ == "__main__":
    main()