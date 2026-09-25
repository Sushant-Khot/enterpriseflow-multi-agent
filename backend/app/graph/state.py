from typing import Any, TypedDict


class AgentState(TypedDict, total=False):

    # Request information
    request_id: str
    workflow_id: str
    user_id: str
    user_role: str
    user_input: str

    # Orchestration
    intent: str
    confidence: float
    selected_agent: str
    routing_reason: str
    routing_source: str
    authorization_status: str

    # Security
    security_status: str
    pii_detected: bool

    # Human approval
    requires_human_approval: bool
    approval_id: str
    approval_status: str
    human_feedback: str

    # Workflow control
    iteration_count: int
    max_iterations: int

    # Agent/tool data
    tool_results: dict[str, Any]

    # Output
    response: str
    status: str
    error: str