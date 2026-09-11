from backend.app.rag.document_chunker import chunk_documents
from backend.app.rag.document_loader import load_knowledge_base
from backend.app.rag.embeddings import embed_documents


def test_embeddings_cover_all_knowledge_base_chunks():
    documents = load_knowledge_base()
    assert len(documents) == 15

    chunks = chunk_documents(documents)
    embedded_documents = embed_documents(chunks)

    assert len(embedded_documents) == len(chunks)
    assert all(
        embedded.embedding
        and all(isinstance(value, (int, float)) for value in embedded.embedding)
        for embedded in embedded_documents
    )
    assert len({len(embedded.embedding) for embedded in embedded_documents}) == 1
    assert all(embedded.document.metadata.get("source") for embedded in embedded_documents)