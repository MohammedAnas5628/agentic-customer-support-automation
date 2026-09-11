from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.tools.ticket_tools import (
    TicketToolResult,
    create_ticket_tool,
    update_ticket_tool,
)


ALLOWED_REASONS = frozenset(
    {
        "human_requested",
        "no_context",
        "security_risk",
        "safety_risk",
        "financial_dispute",
        "policy_exception",
        "unresolved_issue",
        "complex_issue",
    }
)
URGENT_REASONS = frozenset({"security_risk", "safety_risk"})
HIGH_REASONS = frozenset({"financial_dispute", "complex_issue"})


@dataclass(frozen=True)
class EscalationResult:
    success: bool
    message: str
    reason: str
    priority: str
    ticket_number: str | None = None


def _priority_for_reason(reason: str) -> str:
    if reason in URGENT_REASONS:
        return "urgent"
    if reason in HIGH_REASONS:
        return "high"
    return "normal"


async def escalate_to_human(
    session: AsyncSession,
    *,
    reason: str,
    summary: str,
    customer_id: int | None = None,
    ticket_number: str | None = None,
    order_number: str | None = None,
) -> EscalationResult:
    """Create or update a validated support ticket for human review."""
    reason = reason.strip().lower()
    if reason not in ALLOWED_REASONS:
        return EscalationResult(False, "I couldn't validate the escalation reason.", reason, "normal")
    if not summary.strip() or len(summary.strip()) > 5000:
        return EscalationResult(False, "A concise escalation summary is required.", reason, "normal")
    priority = _priority_for_reason(reason)

    if ticket_number is not None:
        result = await update_ticket_tool(
            session,
            ticket_number,
            {"status": "pending", "priority": priority, "description": summary.strip()},
        )
        if not result.success:
            return EscalationResult(False, result.message, reason, priority)
        return EscalationResult(
            True,
            f"Your issue has been escalated for human review under ticket {ticket_number.upper()}.",
            reason,
            priority,
            ticket_number.upper(),
        )

    if customer_id is None or customer_id <= 0:
        return EscalationResult(
            False,
            "I can escalate this, but I need a valid customer reference or ticket number first.",
            reason,
            priority,
        )

    result: TicketToolResult = await create_ticket_tool(
        session,
        customer_id=customer_id,
        order_number=order_number,
        subject="Human support escalation",
        description=summary.strip(),
        status="pending",
        priority=priority,
    )
    if not result.success:
        return EscalationResult(False, result.message, reason, priority)
    created_ticket = str(result.data["ticket_number"]) if result.data else None
    reference = f" under ticket {created_ticket}" if created_ticket else ""
    return EscalationResult(
        True,
        f"Your issue has been escalated for human review{reference}.",
        reason,
        priority,
        created_ticket,
    )