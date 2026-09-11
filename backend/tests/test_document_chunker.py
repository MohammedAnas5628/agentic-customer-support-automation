from backend.app.rag.document_chunker import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    chunk_documents,
)
from backend.app.rag.document_loader import load_knowledge_base


def test_chunks_all_knowledge_base_documents_without_mutating_sources():
    documents = load_knowledge_base()
    original_contents = [document.page_content for document in documents]
    original_metadata = [document.metadata.copy() for document in documents]

    chunks = chunk_documents(documents)

    assert len(documents) == 15
    assert len(chunks) > 1
    assert all(chunk.page_content.strip() for chunk in chunks)
    assert {chunk.metadata["source"] for chunk in chunks} == {
        document.metadata["source"] for document in documents
    }
    assert [document.page_content for document in documents] == original_contents
    assert [document.metadata for document in documents] == original_metadata
    assert CHUNK_SIZE == 1000
    assert CHUNK_OVERLAP == 200