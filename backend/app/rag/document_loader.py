from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document


def load_knowledge_base(knowledge_base_path: str | Path | None = None) -> list[Document]:
    """Load the root knowledge-base Markdown files as LangChain documents."""
    knowledge_base = (
        Path(knowledge_base_path)
        if knowledge_base_path is not None
        else Path(__file__).resolve().parents[3] / "knowledge_base"
    )

    if not knowledge_base.is_dir():
        raise FileNotFoundError(f"Knowledge base directory not found: {knowledge_base}")

    markdown_files = list(knowledge_base.glob("*.md"))
    if not markdown_files:
        raise ValueError(f"Knowledge base contains no Markdown files: {knowledge_base}")

    documents = DirectoryLoader(
        str(knowledge_base),
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=False,
    ).load()

    for document in documents:
        document.metadata["source"] = Path(document.metadata["source"]).name

    return documents