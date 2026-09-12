from backend.app.rag.document_chunker import chunk_documents
from backend.app.rag.document_loader import load_knowledge_base
from backend.app.rag import embeddings


class FakeModel:
    def __init__(self, model_name):
        self.model_name = model_name

    def encode(self, texts, **kwargs):
        assert kwargs["normalize_embeddings"] is True
        return [[0.0] * embeddings.EMBEDDING_DIMENSION for _text in texts]


def test_bge_embedding_model_initializes_locally(monkeypatch):
    created = []
    monkeypatch.setattr(
        embeddings,
        "SentenceTransformer",
        lambda model_name: created.append(model_name) or FakeModel(model_name),
    )
    embeddings._get_model.cache_clear()

    embeddings.embed_query("What is the return policy?")

    assert created == [embeddings.EMBEDDING_MODEL]
    embeddings._get_model.cache_clear()


def test_embeddings_cover_all_knowledge_base_chunks(monkeypatch):
    documents = load_knowledge_base()
    assert len(documents) == 15

    chunks = chunk_documents(documents)
    monkeypatch.setattr(embeddings, "_get_model", lambda: FakeModel(embeddings.EMBEDDING_MODEL))
    embedded_documents = embeddings.embed_documents(chunks)

    assert len(embedded_documents) == len(chunks)
    assert all(
        embedded.embedding
        and all(isinstance(value, (int, float)) for value in embedded.embedding)
        for embedded in embedded_documents
    )
    assert {len(embedded.embedding) for embedded in embedded_documents} == {
        embeddings.EMBEDDING_DIMENSION
    }
    assert all(embedded.document.metadata.get("source") for embedded in embedded_documents)


def test_query_embedding_has_expected_dimension(monkeypatch):
    monkeypatch.setattr(embeddings, "_get_model", lambda: FakeModel(embeddings.EMBEDDING_MODEL))

    vector = embeddings.embed_query("How long does delivery take?")

    assert len(vector) == embeddings.EMBEDDING_DIMENSION