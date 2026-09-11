from backend.app.rag.document_chunker import chunk_documents
from backend.app.rag.document_loader import load_knowledge_base
from backend.app.rag import embeddings


def test_embeddings_cover_all_knowledge_base_chunks(monkeypatch):
    documents = load_knowledge_base()
    assert len(documents) == 15

    chunks = chunk_documents(documents)
    monkeypatch.setattr(
        embeddings,
        "GoogleGenerativeAIEmbeddings",
        lambda **_kwargs: type(
            "FakeEmbeddings",
            (),
            {
                "embed_documents": lambda _self, texts: [
                    [0.0] * 3072 for _text in texts
                ]
            },
        )(),
    )
    embedded_documents = embeddings.embed_documents(chunks)

    assert len(embedded_documents) == len(chunks)
    assert all(
        embedded.embedding
        and all(isinstance(value, (int, float)) for value in embedded.embedding)
        for embedded in embedded_documents
    )
    assert len({len(embedded.embedding) for embedded in embedded_documents}) == 1
    assert all(embedded.document.metadata.get("source") for embedded in embedded_documents)