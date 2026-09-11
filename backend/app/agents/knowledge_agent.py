from backend.app.core.config import settings
from backend.app.db.database import AsyncSessionLocal
from backend.app.rag.generation import GroundedAnswer, generate_grounded_answer
from backend.app.rag.retrieval import retrieve_chunks


async def run_knowledge_agent(
    question: str,
    top_k: int | None = None,
    relevance_threshold: float | None = None,
) -> GroundedAnswer:
    """Orchestrate retrieval and grounded generation for knowledge questions."""
    async with AsyncSessionLocal() as session:
        chunks = await retrieve_chunks(
            session,
            question,
            top_k=top_k if top_k is not None else settings.rag_top_k,
            relevance_threshold=(
                relevance_threshold
                if relevance_threshold is not None
                else settings.rag_relevance_threshold
            ),
        )
    return await generate_grounded_answer(question, chunks)