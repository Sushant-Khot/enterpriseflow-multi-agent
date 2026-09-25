from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from backend.app.graph.state import AgentState

from backend.app.services.langgraph_checkpointer import (
    get_checkpointer,
)

from backend.app.agents.orchestrator import (
    classify_request,
)

from backend.app.agents.blog_agent import (
    blog_agent,
)

from backend.app.agents.background_agent import (
    background_agent,
)

from backend.app.agents.salary_agent import (
    salary_agent,
)

from backend.app.agents.support_agent import (
    support_agent,
)
from backend.app.core.rbac import (
    allowed_intent,
)


# =====================================================
# Security Gate
# =====================================================

def security_gate(
    state: AgentState,
) -> dict:

    return {
        "security_status": "PASSED",
        "pii_detected": False,
    }


# =====================================================
# Orchestrator
# =====================================================

def orchestrator_node(
    state: AgentState,
) -> dict:

    decision = classify_request(
        state["user_input"]
    )

    employee_data = state.get("tool_results", {}).get(
        "employee_data",
        {},
    )
    authorized = allowed_intent(
        role=state.get("user_role", ""),
        intent=decision.intent,
        employee_id=employee_data.get("employee_id"),
        user_id=state.get("user_id"),
    )

    if not authorized:
        return {
            "intent": decision.intent,
            "confidence": decision.confidence,
            "selected_agent": "NONE",
            "routing_reason": decision.reason,
            "routing_source": getattr(
                decision,
                "source",
                "orchestrator",
            ),
            "authorization_status": "DENIED",
            "status": "FORBIDDEN",
            "error": "The current role is not authorized for this request.",
            "response": "You are not authorized to perform this action.",
        }

    return {
        "intent": decision.intent,
        "confidence": decision.confidence,
        "selected_agent": decision.agent,
        "routing_reason": decision.reason,
        "routing_source": getattr(
            decision,
            "source",
            "orchestrator",
        ),
        "authorization_status": "AUTHORIZED",
    }


# =====================================================
# Routing
# =====================================================

def route_agent(
    state: AgentState,
):

    if state.get("authorization_status") == "DENIED":
        return "access_denied"

    agent = state.get(
        "selected_agent"
    )

    if agent == "A1_BLOG":
        return "a1_blog"

    if agent == "A2_BACKGROUND":
        return "a2_background"

    if agent == "A3_SALARY":
        return "a3_salary"

    if agent == "A4_SUPPORT":
        return "a4_support"

    return "a4_support"


def access_denied_node(
    state: AgentState,
) -> dict:
    return {
        "status": "FORBIDDEN",
        "response": "You are not authorized to perform this action.",
        "requires_human_approval": False,
    }


# =====================================================
# A1 routing after review
# =====================================================

def route_blog_result(
    state: AgentState,
):

    status = state.get(
        "status",
        "",
    )

    if status == "REVISION_REQUESTED":

        return "a1_blog"

    return END


# =====================================================
# Build graph
# =====================================================

builder = StateGraph(
    AgentState
)


builder.add_node(
    "security_gate",
    security_gate,
)

builder.add_node(
    "orchestrator",
    orchestrator_node,
)

builder.add_node(
    "a1_blog",
    blog_agent,
)

builder.add_node(
    "a2_background",
    background_agent,
)

builder.add_node(
    "a3_salary",
    salary_agent,
)

builder.add_node(
    "a4_support",
    support_agent,
)

builder.add_node(
    "access_denied",
    access_denied_node,
)


# =====================================================
# Graph edges
# =====================================================

builder.add_edge(
    START,
    "security_gate",
)

builder.add_edge(
    "security_gate",
    "orchestrator",
)


builder.add_conditional_edges(
    "orchestrator",
    route_agent,
    {
        "a1_blog": "a1_blog",
        "a2_background": "a2_background",
        "a3_salary": "a3_salary",
        "a4_support": "a4_support",
        "access_denied": "access_denied",
    },
)


# A1 can either finish or loop
builder.add_conditional_edges(
    "a1_blog",
    route_blog_result,
    {
        "a1_blog": "a1_blog",
        END: END,
    },
)


builder.add_edge(
    "a2_background",
    END,
)

builder.add_edge(
    "a3_salary",
    END,
)

builder.add_edge(
    "a4_support",
    END,
)

builder.add_edge(
    "access_denied",
    END,
)


# =====================================================
# Checkpointer
# =====================================================

checkpointer = get_checkpointer()


workflow_app = builder.compile(
    checkpointer=checkpointer,
)