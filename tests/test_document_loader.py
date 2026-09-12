from pathlib import Path

from backend.app.rag.document_loader import load_knowledge_base


EXPECTED_FILENAMES = {
    path.name for path in (Path(__file__).parents[1] / "knowledge_base").glob("*.md")
}


def test_loads_all_knowledge_base_documents():
    documents = load_knowledge_base()

    assert len(documents) == 15
    assert {document.metadata["source"] for document in documents} == EXPECTED_FILENAMES