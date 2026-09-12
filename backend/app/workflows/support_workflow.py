import asyncio
import logging
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from backend.app.agents.knowledge_agent import run_knowledge_agent
from backend.app.agents.catalog_agent import run_catalog_agent
from backend.app.agents.order_agent import run_order_agent
from backend.app.agents.support_agent import run_support_agent
from backend.app.agents.escalation_agent import run_escalation_agent


logger = logging.getLogger(__name__)


Intent = Literal["catalog", "knowledge", "order", "support", "escalation", "unknown"]


class SupportState(TypedDict, total=False):
    user_message: str
    intent: str
    selected_agent: str
    final_response: str
    escalation_status: str
    executed_nodes: list[str]
    retrieved_context: list[dict]
    sources: list[dict]
    retrieval_score: float | None
    rag_status: str
    order_tool: str
    support_tool: str
    escalation_reason: str
    handoff_reference: str | None
    authenticated_customer_id: int | None
    authenticated_role: str


def _record_node(state: SupportState, node_name: str) -> list[str]:
    return [*state.get("executed_nodes", []), node_name]


def router_node(state: SupportState) -> SupportState:
    return {
        "executed_nodes": _record_node(state, "router"),
    }


async def knowledge_node(state: SupportState) -> SupportState:
    try:
        result = await run_knowledge_agent(state["user_message"])
    except Exception:
        logger.exception("Knowledge Agent failed while handling a customer question")
        return {
            "selected_agent": "knowledge",
            "final_response": (
                "I couldn't access ElectroMart's knowledge base right now. "
                "Please try again or contact customer support."
            ),
            "escalation_status": "recommended",
            "rag_status": "error",
            "executed_nodes": _record_node(state, "knowledge"),
        }
    return {
        "selected_agent": "knowledge",
        "final_response": result.answer,
        "escalation_status": (
            "recommended" if result.status == "no_context" else "not_required"
        ),
        "retrieved_context": result.context,
        "sources": result.sources,
        "retrieval_score": max(
            (item["similarity"] for item in result.context),
            default=None,
        ),
        "rag_status": result.status,
        "executed_nodes": _record_node(state, "knowledge"),
    }


async def catalog_node(state: SupportState) -> SupportState:
    try:
        answer = await run_catalog_agent(state["user_message"])
    except Exception:
        logger.exception("Catalog Agent failed while handling a product question")
        return {
            "selected_agent": "catalog",
            "final_response": "I couldn't access the product catalog right now. Please try again shortly.",
            "escalation_status": "recommended",
            "catalog_status": "error",
            "executed_nodes": _record_node(state, "catalog"),
        }
    return {
        "selected_agent": "catalog",
        "final_response": answer,
        "escalation_status": "not_required",
        "catalog_status": "answered",
        "executed_nodes": _record_node(state, "catalog"),
    }


async def order_node(state: SupportState) -> SupportState:
    try:
        if "authenticated_customer_id" in state or "authenticated_role" in state:
            result = await run_order_agent(
                state["user_message"],
                actor_customer_id=state.get("authenticated_customer_id"),
                actor_role=state.get("authenticated_role", "customer"),
            )
        else:
            result = await run_order_agent(state["user_message"])
    except Exception:
        logger.exception("Order Agent failed while handling a customer question")
        return {
            "selected_agent": "order",
            "final_response": (
                "I couldn't access the order system right now. "
                "Please try again or contact customer support."
            ),
            "escalation_status": "recommended",
            "order_tool": "error",
            "executed_nodes": _record_node(state, "order"),
        }
    return {
        "selected_agent": "order",
        "final_response": result.message,
        "escalation_status": "not_required" if result.success else "recommended",
        "order_tool": result.tool,
        "executed_nodes": _record_node(state, "order"),
    }


async def support_node(state: SupportState) -> SupportState:
    try:
        if "authenticated_customer_id" in state or "authenticated_role" in state:
            result = await run_support_agent(
                state["user_message"],
                actor_customer_id=state.get("authenticated_customer_id"),
                actor_role=state.get("authenticated_role", "customer"),
            )
        else:
            result = await run_support_agent(state["user_message"])
    except Exception:
        logger.exception("Support Agent failed while handling a customer question")
        return {
            "selected_agent": "support",
            "final_response": (
                "I couldn't access the support ticket system right now. "
                "Please try again or contact customer support."
            ),
            "escalation_status": "recommended",
            "support_tool": "error",
            "executed_nodes": _record_node(state, "support"),
        }
    return {
        "selected_agent": "support",
        "final_response": result.message,
        "escalation_status": "not_required" if result.success else "recommended",
        "support_tool": result.tool,
        "executed_nodes": _record_node(state, "support"),
    }


async def escalation_node(state: SupportState) -> SupportState:
    try:
        result = await run_escalation_agent(
            state["user_message"],
            customer_id=state.get("authenticated_customer_id"),
            rag_status=state.get("rag_status"),
        )
    except Exception:
        logger.exception("Escalation Agent failed while handling a customer question")
        return {
            "selected_agent": "escalation",
            "final_response": (
                "I couldn't complete the human handoff right now. "
                "Please try again or contact customer support."
            ),
            "escalation_status": "error",
            "escalation_reason": "system_error",
            "executed_nodes": _record_node(state, "escalation"),
        }
    return {
        "selected_agent": "escalation",
        "final_response": result.message,
        "escalation_status": "pending" if result.success else "recommended",
        "escalation_reason": result.reason,
        "handoff_reference": result.ticket_number,
        "executed_nodes": _record_node(state, "escalation"),
    }


def fallback_node(state: SupportState) -> SupportState:
    return {
        "selected_agent": "fallback",
        "final_response": "I cannot determine which support capability should handle this request yet.",
        "escalation_status": "not_required",
        "executed_nodes": _record_node(state, "fallback"),
    }


def route_by_intent(state: SupportState) -> str:
    return {
        "catalog": "catalog",
        "knowledge": "knowledge",
        "order": "order",
        "support": "support",
        "escalation": "escalation",
    }.get(state.get("intent", "unknown"), "fallback")


def build_support_graph():
    graph = StateGraph(SupportState)
    graph.add_node("router", router_node)
    graph.add_node("catalog", catalog_node)
    graph.add_node("knowledge", knowledge_node)
    graph.add_node("order", order_node)
    graph.add_node("support", support_node)
    graph.add_node("escalation", escalation_node)
    graph.add_node("fallback", fallback_node)
    graph.add_edge(START, "router")
    graph.add_conditional_edges(
        "router",
        route_by_intent,
        {
            "catalog": "catalog",
            "knowledge": "knowledge",
            "order": "order",
            "support": "support",
            "escalation": "escalation",
            "fallback": "fallback",
        },
    )
    for node_name in ("catalog", "knowledge", "order", "support", "escalation", "fallback"):
        graph.add_edge(node_name, END)
    return graph.compile()


support_graph = build_support_graph()


async def run_support_workflow_async(
    user_message: str,
    intent: str,
    *,
    authenticated_customer_id: int | None = None,
    authenticated_role: str | None = None,
) -> SupportState:
    """Run the workflow in async applications such as FastAPI."""
    initial_state: SupportState = {
            "user_message": user_message,
            "intent": intent,
            "executed_nodes": [],
    }
    if authenticated_customer_id is not None:
        initial_state["authenticated_customer_id"] = authenticated_customer_id
    if authenticated_role is not None:
        initial_state["authenticated_role"] = authenticated_role
    return await support_graph.ainvoke(initial_state)


def run_support_workflow(user_message: str, intent: str) -> SupportState:
    """Synchronous compatibility wrapper for scripts and tests."""
    return asyncio.run(run_support_workflow_async(user_message, intent))
