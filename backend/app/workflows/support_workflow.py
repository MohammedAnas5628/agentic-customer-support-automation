import asyncio
import logging
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from backend.app.agents.knowledge_agent import run_knowledge_agent


logger = logging.getLogger(__name__)


Intent = Literal["knowledge", "order", "support", "escalation", "unknown"]


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


def order_node(state: SupportState) -> SupportState:
    return {
        "selected_agent": "order",
        "final_response": "Order agent capability is not implemented yet.",
        "escalation_status": "not_required",
        "executed_nodes": _record_node(state, "order"),
    }


def support_node(state: SupportState) -> SupportState:
    return {
        "selected_agent": "support",
        "final_response": "Support agent capability is not implemented yet.",
        "escalation_status": "not_required",
        "executed_nodes": _record_node(state, "support"),
    }


def escalation_node(state: SupportState) -> SupportState:
    return {
        "selected_agent": "escalation",
        "final_response": "Escalation agent capability is not implemented yet.",
        "escalation_status": "pending",
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
        "knowledge": "knowledge",
        "order": "order",
        "support": "support",
        "escalation": "escalation",
    }.get(state.get("intent", "unknown"), "fallback")


def build_support_graph():
    graph = StateGraph(SupportState)
    graph.add_node("router", router_node)
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
            "knowledge": "knowledge",
            "order": "order",
            "support": "support",
            "escalation": "escalation",
            "fallback": "fallback",
        },
    )
    for node_name in ("knowledge", "order", "support", "escalation", "fallback"):
        graph.add_edge(node_name, END)
    return graph.compile()


support_graph = build_support_graph()


async def run_support_workflow_async(user_message: str, intent: str) -> SupportState:
    """Run the workflow in async applications such as FastAPI."""
    return await support_graph.ainvoke(
        {
            "user_message": user_message,
            "intent": intent,
            "executed_nodes": [],
        }
    )


def run_support_workflow(user_message: str, intent: str) -> SupportState:
    """Synchronous compatibility wrapper for scripts and tests."""
    return asyncio.run(run_support_workflow_async(user_message, intent))