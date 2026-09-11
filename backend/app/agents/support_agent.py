import re

from backend.app.db.database import AsyncSessionLocal
from backend.app.tools.ticket_tools import (
    TicketToolResult,
    create_ticket_tool,
    get_ticket_tool,
    update_ticket_tool,
)


INVALID_TICKET_RESPONSE = (
    "Please provide a valid ticket number, such as TKT10001, or the required "
    "customer details so I can help."
)
TICKET_PATTERN = re.compile(r"\bTKT[A-Z0-9]{1,27}\b", re.IGNORECASE)
CUSTOMER_PATTERN = re.compile(r"\bcustomer(?:_id| id)\s*[:=]?\s*(\d+)\b", re.IGNORECASE)


def _ticket_number(message: str) -> str | None:
    match = TICKET_PATTERN.search(message)
    return match.group(0).upper() if match else None


def _select_tool(message: str):
    lowered = message.lower()
    if re.search(r"\b(update|change|edit|modify)\b", lowered):
        return update_ticket_tool
    if re.search(r"\b(status|track|progress|find|show|get)\b", lowered):
        return get_ticket_tool
    return create_ticket_tool


async def run_support_agent(
    message: str,
    *,
    actor_customer_id: int | None = None,
    actor_role: str = "customer",
) -> TicketToolResult:
    """Select a ticket tool; all validation and persistence stays in the tool/service layer."""
    tool = _select_tool(message)
    ticket_number = _ticket_number(message)
    async with AsyncSessionLocal() as session:
        if tool is get_ticket_tool:
            if ticket_number is None:
                return TicketToolResult(False, "support_agent", INVALID_TICKET_RESPONSE)
            return await get_ticket_tool(
                session,
                ticket_number,
                actor_customer_id=actor_customer_id,
                actor_role=actor_role,
            )
        if tool is update_ticket_tool:
            if ticket_number is None:
                return TicketToolResult(False, "support_agent", INVALID_TICKET_RESPONSE)
            changes: dict[str, str] = {}
            lowered = message.lower()
            for status in ("open", "pending", "in_progress", "resolved", "closed"):
                if status.replace("_", " ") in lowered:
                    changes["status"] = status
                    break
            for priority in ("low", "normal", "high", "urgent"):
                if priority in lowered:
                    changes["priority"] = priority
                    break
            if not changes:
                return TicketToolResult(False, "support_agent", "Please specify the ticket change.")
            return await update_ticket_tool(
                session,
                ticket_number,
                changes,
                actor_customer_id=actor_customer_id,
                actor_role=actor_role,
            )

        customer_match = CUSTOMER_PATTERN.search(message)
        if customer_match is None:
            return TicketToolResult(False, "support_agent", INVALID_TICKET_RESPONSE)
        subject = message[:200].strip()
        return await create_ticket_tool(
            session,
            customer_id=int(customer_match.group(1)),
            subject=subject or "Customer support request",
            description=message,
            actor_customer_id=actor_customer_id,
            actor_role=actor_role,
        )