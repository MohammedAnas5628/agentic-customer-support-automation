from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate
from backend.app.services.ticket_service import (
    create_ticket,
    get_ticket_by_number,
    update_ticket,
)


router = APIRouter(prefix="/api/tickets", tags=["tickets"])


@router.get("/{ticket_number}", response_model=TicketResponse)
async def read_ticket(
    ticket_number: str,
    session: AsyncSession = Depends(get_db),
) -> TicketResponse:
    ticket = await get_ticket_by_number(session, ticket_number)
    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return ticket


@router.post("", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_support_ticket(
    payload: TicketCreate,
    session: AsyncSession = Depends(get_db),
) -> TicketResponse:
    ticket = await create_ticket(session, **payload.model_dump())
    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer or related order not found",
        )

    return ticket


@router.patch("/{ticket_number}", response_model=TicketResponse)
async def update_support_ticket(
    ticket_number: str,
    payload: TicketUpdate,
    session: AsyncSession = Depends(get_db),
) -> TicketResponse:
    ticket = await update_ticket(
        session,
        ticket_number,
        payload.model_dump(exclude_unset=True, exclude_none=True),
    )
    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return ticket