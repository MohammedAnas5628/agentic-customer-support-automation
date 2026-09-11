import re
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.services.ticket_service import (
    create_ticket as create_ticket_service,
    get_ticket_by_number,
    update_ticket as update_ticket_service,
)


TICKET_NUMBER_PATTERN = re.compile(r"^TKT[A-Z0-9]{1,27}$", re.IGNORECASE)
ORDER_NUMBER_PATTERN = re.compile(r"^(?:EM|ORD|ORDER)[-_]?\d+$", re.IGNORECASE)
ALLOWED_STATUSES = frozenset({"open", "pending", "in_progress", "resolved", "closed"})
ALLOWED_PRIORITIES = frozenset({"low", "normal", "high", "urgent"})
MAX_DESCRIPTION_LENGTH = 5000


@dataclass(frozen=True)
class TicketToolResult:
    success: bool
    tool: str
    message: str
    data: dict[str, object] | None = None


def _valid_ticket_number(ticket_number: str) -> bool:
    return bool(TICKET_NUMBER_PATTERN.fullmatch(ticket_number.strip()))


def _validate_text(value: str, field: str, maximum: int) -> str | None:
    cleaned = value.strip()
    if not cleaned:
        return f"{field.capitalize()} is required."
    if len(cleaned) > maximum:
        return f"{field.capitalize()} is too long."
    return None


async def create_ticket_tool(
    session: AsyncSession,
    *,
    customer_id: int,
    subject: str,
    description: str,
    order_number: str | None = None,
    status: str = "open",
    priority: str = "normal",
    actor_customer_id: int | None = None,
    actor_role: str = "customer",
) -> TicketToolResult:
    if actor_role == "customer" and actor_customer_id is not None:
        customer_id = actor_customer_id
    if customer_id <= 0:
        return TicketToolResult(False, "create_ticket", "A valid customer ID is required.")
    subject_error = _validate_text(subject, "subject", 200)
    description_error = _validate_text(description, "description", MAX_DESCRIPTION_LENGTH)
    if subject_error or description_error:
        return TicketToolResult(
            False,
            "create_ticket",
            subject_error or description_error or "Invalid ticket details.",
        )
    status = status.strip().lower()
    priority = priority.strip().lower()
    if status not in ALLOWED_STATUSES:
        return TicketToolResult(False, "create_ticket", "That ticket status is not allowed.")
    if priority not in ALLOWED_PRIORITIES:
        return TicketToolResult(False, "create_ticket", "That ticket priority is not allowed.")
    if order_number is not None:
        order_number = order_number.strip().upper()
        if not ORDER_NUMBER_PATTERN.fullmatch(order_number):
            return TicketToolResult(False, "create_ticket", "That order number is invalid.")

    ticket = await create_ticket_service(
        session,
        customer_id=customer_id,
        order_number=order_number,
        subject=subject.strip(),
        description=description.strip(),
        status=status,
        priority=priority,
    )
    if ticket is None:
        return TicketToolResult(
            False,
            "create_ticket",
            "I couldn't validate the customer or related order for this ticket.",
        )
    return TicketToolResult(
        True,
        "create_ticket",
        f"Support ticket {ticket.ticket_number} was created.",
        {"ticket_number": ticket.ticket_number, "status": ticket.status},
    )


async def get_ticket_tool(
    session: AsyncSession,
    ticket_number: str,
    *,
    actor_customer_id: int | None = None,
    actor_role: str = "customer",
) -> TicketToolResult:
    ticket_number = ticket_number.strip().upper()
    if not _valid_ticket_number(ticket_number):
        return TicketToolResult(False, "get_ticket", "That ticket number is invalid.")
    ticket = await get_ticket_by_number(session, ticket_number)
    if ticket is None or (
        actor_role == "customer"
        and actor_customer_id is not None
        and ticket.customer_id != actor_customer_id
    ):
        return TicketToolResult(False, "get_ticket", "I couldn't find that ticket.")
    return TicketToolResult(
        True,
        "get_ticket",
        f"Ticket {ticket.ticket_number} is {ticket.status} with {ticket.priority} priority.",
        {"ticket_number": ticket.ticket_number, "status": ticket.status, "priority": ticket.priority},
    )


async def update_ticket_tool(
    session: AsyncSession,
    ticket_number: str,
    changes: dict[str, str],
    *,
    actor_customer_id: int | None = None,
    actor_role: str = "customer",
) -> TicketToolResult:
    ticket_number = ticket_number.strip().upper()
    if not _valid_ticket_number(ticket_number):
        return TicketToolResult(False, "update_ticket", "That ticket number is invalid.")
    if actor_role == "customer" and actor_customer_id is not None:
        ticket = await get_ticket_by_number(session, ticket_number)
        if ticket is None or ticket.customer_id != actor_customer_id:
            return TicketToolResult(False, "update_ticket", "I couldn't find that ticket.")
    if not changes or any(field not in {"subject", "description", "status", "priority"} for field in changes):
        return TicketToolResult(False, "update_ticket", "No valid ticket changes were provided.")

    normalized: dict[str, str] = {}
    for field, value in changes.items():
        if field == "subject":
            error = _validate_text(value, field, 200)
        elif field == "description":
            error = _validate_text(value, field, MAX_DESCRIPTION_LENGTH)
        else:
            error = None
        if error:
            return TicketToolResult(False, "update_ticket", error)
        normalized[field] = value.strip().lower() if field in {"status", "priority"} else value.strip()

    if "status" in normalized and normalized["status"] not in ALLOWED_STATUSES:
        return TicketToolResult(False, "update_ticket", "That ticket status is not allowed.")
    if "priority" in normalized and normalized["priority"] not in ALLOWED_PRIORITIES:
        return TicketToolResult(False, "update_ticket", "That ticket priority is not allowed.")

    ticket = await update_ticket_service(session, ticket_number, normalized)
    if ticket is None:
        return TicketToolResult(False, "update_ticket", "I couldn't find that ticket.")
    return TicketToolResult(
        True,
        "update_ticket",
        f"Ticket {ticket.ticket_number} was updated.",
        {"ticket_number": ticket.ticket_number, "status": ticket.status, "priority": ticket.priority},
    )