from pydantic import BaseModel, Field

from backend.app.schemas.rag import RagSource


class SupportQueryRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class SupportQueryResponse(BaseModel):
    answer: str
    sources: list[RagSource] = []
    status: str
    intent: str
    escalation_status: str | None = None
    ticket_number: str | None = None
