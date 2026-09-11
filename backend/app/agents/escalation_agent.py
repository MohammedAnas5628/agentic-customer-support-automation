import re

from backend.app.db.database import AsyncSessionLocal
from backend.app.tools.escalation_tools import EscalationResult, escalate_to_human


CUSTOMER_PATTERN = re.compile(r"\bcustomer(?:_id| id)\s*[:=]?\s*(\d+)\b", re.IGNORECASE)
TICKET_PATTERN = re.compile(r"\bTKT[A-Z0-9]{1,27}\b", re.IGNORECASE)
ORDER_PATTERN = re.compile(r"\b(?:EM|ORD|ORDER)[-_]?\d+\b", re.IGNORECASE)


def infer_escalation_reason(message: str, rag_status: str | None = None) -> str:
    lowered = message.lower()
    if rag_status == "no_context":
        return "no_context"
    if re.search(r"\b(human|manager|representative|agent)\b", lowered):
        return "human_requested"
    if re.search(r"\b(password|otp|unauthorized|fraud|compromised|hacked)\b", lowered):
        return "security_risk"
    if re.search(r"\b(safety|fire|shock|dangerous|injury)\b", lowered):
        return "safety_risk"
    if re.search(r"\b(dispute|duplicate charge|charged twice|financial)\b", lowered):
        return "financial_dispute"
    if re.search(r"\b(exception|outside policy|legal|lawyer|regulator)\b", lowered):
        return "policy_exception"
    return "complex_issue"


def _number(pattern: re.Pattern[str], message: str) -> str | None:
    match = pattern.search(message)
    return match.group(0).upper() if match else None


async def run_escalation_agent(
    message: str,
    *,
    customer_id: int | None = None,
    ticket_number: str | None = None,
    order_number: str | None = None,
    rag_status: str | None = None,
) -> EscalationResult:
    """Prepare a bounded handoff request and delegate validation to the tool."""
    reason = infer_escalation_reason(message, rag_status)
    customer_match = CUSTOMER_PATTERN.search(message)
    resolved_customer_id = customer_id or (
        int(customer_match.group(1)) if customer_match else None
    )
    return await _run_handoff(
        message,
        reason=reason,
        customer_id=resolved_customer_id,
        ticket_number=ticket_number or _number(TICKET_PATTERN, message),
        order_number=order_number or _number(ORDER_PATTERN, message),
    )


async def _run_handoff(message: str, **kwargs) -> EscalationResult:
    async with AsyncSessionLocal() as session:
        return await escalate_to_human(session, summary=message, **kwargs)