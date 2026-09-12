from backend.app.core.config import settings
from backend.app.db.database import AsyncSessionLocal
from backend.app.rag.generation import GroundedAnswer, generate_grounded_answer
from backend.app.rag.retrieval import retrieve_chunks


def query_variants(question: str) -> list[str]:
    """Add focused paraphrases without changing the customer's original query."""
    normalized = " ".join(question.lower().strip().split())
    variants = [question]
    families = (
        (("return", "returns", "return window", "return something"), "return policy product return eligibility"),
        (("shipping", "delivery", "arrive", "order arrive"), "shipping delivery time arrival"),
        (("warranty", "guarantee", "repair"), "warranty coverage duration repair"),
        (("payment", "pay", "card", "upi"), "payment methods checkout accepted payments"),
        (("cancel", "cancellation"), "cancellation policy cancel order"),
    )
    for terms, expansion in families:
        if any(term in normalized for term in terms):
            variants.append(expansion)
    return variants


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
            query_variants=query_variants(question),
        )
    return await generate_grounded_answer(question, chunks)