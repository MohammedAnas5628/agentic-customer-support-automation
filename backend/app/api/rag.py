from fastapi import APIRouter
import logging

from backend.app.agents.knowledge_agent import run_knowledge_agent
from backend.app.schemas.rag import RagQueryRequest, RagQueryResponse, RagSource


router = APIRouter(prefix="/api/rag", tags=["rag"])
logger = logging.getLogger(__name__)


@router.post("/query", response_model=RagQueryResponse)
async def query_knowledge_base(request: RagQueryRequest) -> RagQueryResponse:
    try:
        result = await run_knowledge_agent(request.query)
    except Exception:
        logger.exception("RAG query failed")
        return RagQueryResponse(
            answer=(
                "I couldn't access ElectroMart's knowledge base right now. "
                "Please try again or contact customer support."
            ),
            sources=[],
            status="error",
        )
    return RagQueryResponse(
        answer=result.answer,
        sources=[RagSource(**source) for source in result.sources],
        status=result.status,
    )