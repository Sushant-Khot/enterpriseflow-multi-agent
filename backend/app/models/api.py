from typing import Any, Literal

from pydantic import BaseModel, Field


UserRole = Literal["EMPLOYEE", "HR_ADMIN", "SUPPORT_ADMIN"]


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=10000,
    )

    user_id: str = Field(
        min_length=1,
        max_length=100,
    )

    user_role: UserRole = "EMPLOYEE"

    context: dict[str, Any] = Field(
        default_factory=dict
    )

class ApprovalRequest(BaseModel):
    approved: bool
    feedback: str = ""

class ApprovalResponse(BaseModel):
    approval_id: str
    workflow_id: str
    status: str
    feedback: str

    
class ChatResponse(BaseModel):
    request_id: str
    workflow_id: str
    intent: str
    selected_agent: str
    status: str
    response: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class WorkflowStatusResponse(BaseModel):
    workflow_id: str
    request_id: str
    status: str

    intent: str
    selected_agent: str

    confidence: float = 0.0
    routing_source: str = "unknown"
    routing_reason: str = ""

    iteration_count: int

    response: str

    error: str | None = None


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str
