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
        (("shipping", "delivery", "arrive", "order arrive", "track", "tracking"), "shipping delivery time arrival tracking"),
        (("warranty", "guarantee", "repair", "service center"), "warranty coverage duration repair claim"),
        (("payment", "pay", "card", "upi", "net banking", "cod"), "payment methods checkout accepted payments"),
        (("cancel", "cancellation"), "cancellation policy cancel order"),
        (("replace", "replacement", "exchange", "damaged", "defective", "broken", "wrong item"), "cancellation replacement damaged defective exchange policy"),
        (("invoice", "tax", "gst", "receipt", "bill", "billing"), "invoice tax gst receipt billing download"),
        (("coupon", "discount", "offer", "promo", "voucher", "cashback"), "offers discounts coupons promotional vouchers eligibility"),
        (("account", "password", "login", "reset", "otp", "profile"), "account security login password reset authentication"),
        (("human", "agent", "representative", "contact support", "talk to someone", "phone", "helpline"), "customer support contact human agent escalation helpline"),
        (("specs", "specification", "features", "battery", "compatibility", "catalog"), "product catalog specifications features compatibility details"),
    )
    for terms, expansion in families:
        if any(term in normalized for term in terms):
            variants.append(expansion)
    return variants


async def run_knowledge_agent(
    question: str,
    top_k: int | None = None,
    relevance_threshold: float | None = None,
    conversation_history: list[dict[str, str]] | None = None,
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
    return await generate_grounded_answer(question, chunks, conversation_history=conversation_history)