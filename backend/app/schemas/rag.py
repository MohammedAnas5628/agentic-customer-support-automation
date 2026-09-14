from pydantic import BaseModel, Field


class RagQueryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=4000, pattern=r"^[^\x00-\x08\x0b\x0c\x0e-\x1f\x7f]+$")


class RagSource(BaseModel):
    source: str
    score: float


class RagQueryResponse(BaseModel):
    answer: str
    sources: list[RagSource]
    status: str