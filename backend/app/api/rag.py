from fastapi import APIRouter, Request
import logging

from backend.app.agents.knowledge_agent import run_knowledge_agent
from backend.app.core.limiter import limiter
from backend.app.schemas.rag import RagQueryRequest, RagQueryResponse, RagSource


router = APIRouter(prefix="/api/rag", tags=["rag"])
logger = logging.getLogger(__name__)


@router.post("/query", response_model=RagQueryResponse)
@limiter.limit("30/minute")
async def query_knowledge_base(request: Request, query: RagQueryRequest) -> RagQueryResponse:
    try:
        result = await run_knowledge_agent(query.query)
    except Exception:
        logger.exception("RAG query failed")
        return RagQueryResponse(
            answer=(
                "I don't currently have enough information to answer that accurately. "
                "I can help with ElectroMart products, orders, delivery, returns, warranty, payments, and support."
            ),
            sources=[],
            status="error",
        )
    return RagQueryResponse(
        answer=result.answer,
        sources=[RagSource(**source) for source in result.sources],
        status=result.status,
    )