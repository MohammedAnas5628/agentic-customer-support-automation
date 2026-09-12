import re

from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.core.security import get_optional_current_user
from backend.app.models.customer import Customer
from backend.app.schemas.rag import RagSource
from backend.app.schemas.support import SupportQueryRequest, SupportQueryResponse
from backend.app.workflows.support_workflow import run_support_workflow_async


router = APIRouter(prefix="/api/support", tags=["support"])

_GREETING = re.compile(r"^\s*(hi+|hello+|hey+|heyy+|good (morning|afternoon|evening))\s*[!.?]*\s*$", re.I)
_THANKS = re.compile(r"^\s*(thanks|thank you|thx)\s*[!.?]*\s*$", re.I)
_GOODBYE = re.compile(r"^\s*(bye|goodbye|see you)\s*[!.?]*\s*$", re.I)
_WELLBEING = re.compile(r"\bhow are you\b", re.I)
_CAPABILITIES = re.compile(r"\b(what can you help|what do you help|what can you do)\b", re.I)
_ORDER = re.compile(r"\b(order|tracking|track|delivery status|order status|cancel|refund)\b", re.I)
_ESCALATION = re.compile(r"\b(human|representative|live agent|speak to|talk to|manager)\b", re.I)
_SUPPORT = re.compile(r"\b(complaint|damaged|broken|ticket|replace|replacement|help with my)\b", re.I)
_CATALOG = re.compile(r"\b(product|catalog|laptop|notebook|mobile|phone|smartphone|tablet|headphone|earbud|speaker|soundbar|television|tv|camera|watch|gaming|console|charger|cable|keyboard|mouse|accessor|recommend|suggest|buy)\w*\b|what do you sell|what can i buy|what do you have", re.I)
_KNOWLEDGE = re.compile(r"\b(shipping|delivery|return|replacement|warranty|payment|refund policy|cancellation policy|policy|invoice|offer|discount|account)\b", re.I)

_CAPABILITY_RESPONSE = "I can help with ElectroMart products, orders, delivery, returns, warranty, payments, refunds, and support. What would you like to know?"
_UNSUPPORTED_RESPONSE = "I mainly help with ElectroMart products, orders, delivery, returns, warranty, payments, and support. What can I help you with today?"
_NO_CONTEXT_RESPONSE = "I don't have enough ElectroMart information to answer that clearly. I can help with products, orders, delivery, returns, warranty, payments, or support."


def classify_message(message: str) -> tuple[str, str | None]:
    """Return a bounded support intent or a direct customer-facing reply."""
    if _GREETING.match(message):
        return "conversation", "Hey! Welcome to ElectroMart. How can I help you today?"
    if _THANKS.match(message):
        return "conversation", "You're welcome! I'm here whenever you need a hand with ElectroMart."
    if _GOODBYE.match(message):
        return "conversation", "Goodbye! Thanks for choosing ElectroMart."
    if _WELLBEING.search(message):
        return "conversation", f"I'm doing great! { _CAPABILITY_RESPONSE }"
    if _CAPABILITIES.search(message):
        return "conversation", _CAPABILITY_RESPONSE
    if _ESCALATION.search(message):
        return "escalation", None
    if _ORDER.search(message):
        return "order", None
    if _SUPPORT.search(message):
        return "support", None
    if _KNOWLEDGE.search(message):
        return "knowledge", None
    if _CATALOG.search(message):
        return "catalog", None
    return "unsupported", _UNSUPPORTED_RESPONSE


@router.post("/query", response_model=SupportQueryResponse)
async def query_support(
    request: SupportQueryRequest,
    customer: Customer | None = Depends(get_optional_current_user),
) -> SupportQueryResponse:
    intent, direct_response = classify_message(request.message)
    if direct_response is not None:
        return SupportQueryResponse(answer=direct_response, sources=[], status="answered", intent=intent)
    if intent in {"order", "support", "escalation"} and customer is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please sign in to get help with your order or support request.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    state = await run_support_workflow_async(
        request.message,
        intent,
        authenticated_customer_id=customer.id if customer else None,
        authenticated_role=customer.role if customer else None,
    )
    rag_status = state.get("rag_status")
    answer = state.get("final_response", _UNSUPPORTED_RESPONSE)
    if intent == "knowledge" and rag_status in {"no_context", "error"}:
        answer = _NO_CONTEXT_RESPONSE
    return SupportQueryResponse(
        answer=answer,
        sources=[RagSource(**source) for source in state.get("sources", [])],
        status="answered" if rag_status in {None, "answered"} else "unavailable",
        intent=intent,
        escalation_status=state.get("escalation_status"),
        ticket_number=state.get("handoff_reference"),
    )
