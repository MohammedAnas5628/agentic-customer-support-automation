from pydantic import BaseModel, Field


class RagQueryRequest(BaseModel):
    query: str = Field(min_length=1)


class RagSource(BaseModel):
    source: str
    score: float


class RagQueryResponse(BaseModel):
    answer: str
    sources: list[RagSource]
    status: str