from pydantic import BaseModel, Field

from backend.app.schemas.rag import RagSource


class SupportQueryRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000, pattern=r"^[^\x00-\x08\x0b\x0c\x0e-\x1f\x7f]+$")
    conversation_id: int | None = Field(default=None, gt=0)


class SupportQueryResponse(BaseModel):
    answer: str
    sources: list[RagSource] = []
    status: str
    intent: str
    escalation_status: str | None = None
    ticket_number: str | None = None
    conversation_id: int | None = None
