from fastapi import APIRouter, HTTPException

from langgraph.types import Command

from backend.app.config.settings import get_settings
from backend.app.core.ids import generate_request_id, generate_workflow_id
from backend.app.graph.workflow import workflow_app
from backend.app.models.api import (
    ApprovalRequest,
    ApprovalResponse,
    ChatRequest,
    ChatResponse,
    HealthResponse,
    WorkflowStatusResponse,
)
from backend.app.services.approval_store import approval_store
from backend.app.services.guardrails import (
    apply_guardrail,
)
from backend.app.services.monitoring import (
    record_metric,
)
from backend.app.services.workflow_store import workflow_store

router = APIRouter()
settings = get_settings()


@router.get("/approvals/{approval_id}")
async def get_approval(approval_id: str):
    approval = approval_store.get(approval_id)

    if approval is None:
        raise HTTPException(
            status_code=404,
            detail="Approval not found.",
        )

    return approval


@router.post(
    "/approvals/{approval_id}",
    response_model=ApprovalResponse,
)
async def submit_approval(
    approval_id: str,
    request: ApprovalRequest,
):
    approval = approval_store.get(approval_id)

    if approval is None:
        raise HTTPException(
            status_code=404,
            detail="Approval not found.",
        )

    if approval["status"] != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="Approval already processed.",
        )

    workflow_id = approval["workflow_id"]
    config = {"configurable": {"thread_id": workflow_id}}
    resume_value = {
        "approved": request.approved,
        "feedback": request.feedback,
    }

    try:
        result = workflow_app.invoke(
            Command(resume=resume_value),
            config=config,
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to resume workflow.",
        )

    interrupts = result.get("__interrupt__", ())

    if interrupts:
        return ApprovalResponse(
            approval_id=approval_id,
            workflow_id=workflow_id,
            status="PENDING",
            feedback=request.feedback,
        )

    workflow_store.update(
        workflow_id,
        {
            "status": result.get("status", "COMPLETED"),
            "response": result.get("response", ""),
            "approval_id": result.get("approval_id", approval_id),
            "approval_status": result.get("approval_status"),
            "iteration_count": result.get("iteration_count", 0),
        },
    )

    return ApprovalResponse(
        approval_id=approval_id,
        workflow_id=workflow_id,
        status=result.get("status", "COMPLETED"),
        feedback=request.feedback,
    )


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    request_id = generate_request_id()
    workflow_id = generate_workflow_id()

    try:
        guardrail_input = apply_guardrail(
            text=request.message,
            source="INPUT",
        )

        if not guardrail_input["allowed"]:
            record_metric("GuardrailBlocked")

            return ChatResponse(
                workflow_id="",
                request_id="",
                intent="SECURITY",
                selected_agent="NONE",
                status="SECURITY_BLOCKED",
                response=(
                    "Your request was blocked by the "
                    "EnterpriseFlow security guardrail."
                ),
                metadata={
                    "guardrail": True,
                    "guardrail_action": guardrail_input["action"],
                },
            )

        record_metric("WorkflowRequests")

        initial_state = {
            "request_id": request_id,
            "workflow_id": workflow_id,
            "user_id": request.user_id,
            "user_role": request.user_role,
            "user_input": guardrail_input["text"],
            "iteration_count": 0,
            "max_iterations": settings.max_agent_iterations,
            "status": "RUNNING",
            "tool_results": request.context,
        }

        config = {"configurable": {"thread_id": workflow_id}}
        result = workflow_app.invoke(initial_state, config=config)

        response_text = result.get("response", "")
        guardrail_output = apply_guardrail(
            text=response_text,
            source="OUTPUT",
        )

        if not guardrail_output["allowed"]:
            record_metric("GuardrailBlocked")
            response_text = (
                "The generated response was blocked by the "
                "EnterpriseFlow security guardrail."
            )
        else:
            response_text = guardrail_output["text"]

        interrupts = result.get("__interrupt__", ())

        if interrupts:
            interrupt_value = (
                interrupts[0].value if hasattr(interrupts[0], "value") else interrupts[0]
            )
            approval_id = (
                interrupt_value.get("approval_id")
                if isinstance(interrupt_value, dict)
                else None
            )
            review_text = (
                interrupt_value.get("review", "Human approval required.")
                if isinstance(interrupt_value, dict)
                else "Human approval required."
            )

            workflow_store.create(
                workflow_id,
                {
                    "request_id": request_id,
                    "user_id": request.user_id,
                    "user_role": request.user_role,
                    "message": request.message,
                    "status": "WAITING_FOR_APPROVAL",
                    "intent": "BLOG_REVIEW",
                    "selected_agent": "A1_BLOG",
                    "confidence": 0.0,
                    "response": response_text or review_text,
                    "approval_id": approval_id,
                    "approval_status": "PENDING",
                },
            )

            return ChatResponse(
                workflow_id=workflow_id,
                request_id=request_id,
                status="WAITING_FOR_APPROVAL",
                response=response_text or review_text,
                metadata={
                    "approval_id": approval_id,
                    "approval_status": "PENDING",
                    "requires_human_approval": True,
                    "interrupt": interrupt_value,
                },
                intent="BLOG_REVIEW",
                selected_agent="A1_BLOG",
            )

        workflow_store.create(
            workflow_id,
            {
                "request_id": request_id,
                "user_id": request.user_id,
                "user_role": request.user_role,
                "message": request.message,
                "status": result.get("status", "SUCCESS"),
                "intent": result.get("intent", "UNKNOWN"),
                "selected_agent": result.get("selected_agent", "NONE"),
                "confidence": result.get("confidence", 0.0),
                "routing_source": result.get("routing_source", "unknown"),
                "routing_reason": result.get("routing_reason", ""),
                "iteration_count": result.get("iteration_count", 0),
                "response": result.get("response", ""),
                "approval_id": result.get("approval_id"),
                "approval_status": result.get("approval_status"),
                "error": result.get("error"),
            },
        )

        record_metric("WorkflowCompleted")

        return ChatResponse(
            request_id=request_id,
            workflow_id=workflow_id,
            intent=result.get("intent", "UNKNOWN"),
            selected_agent=result.get("selected_agent", "NONE"),
            status=result.get("status", "SUCCESS"),
            response=response_text,
            metadata={
                "agent": result.get("selected_agent"),
                "intent": result.get("intent"),
                "confidence": result.get("confidence", 0.0),
                "routing_source": result.get("routing_source", "unknown"),
                "routing_reason": result.get("routing_reason", ""),
                "security_status": result.get("security_status", "UNKNOWN"),
                "iteration_count": result.get("iteration_count", 0),
                "requires_human_approval": result.get("requires_human_approval", False),
                "tool_results": result.get("tool_results", {}),
                "approval_id": result.get("approval_id"),
                "approval_status": result.get("approval_status"),
            },
        )
    except Exception as exc:
        record_metric("WorkflowFailed")

        workflow_store.create(
            workflow_id,
            {
                "request_id": request_id,
                "user_id": request.user_id,
                "user_role": request.user_role,
                "message": request.message,
                "status": "FAILED",
                "intent": "UNKNOWN",
                "selected_agent": "UNKNOWN",
                "confidence": 0.0,
                "response": "",
                "error": str(exc),
            },
        )
        raise HTTPException(
            status_code=500,
            detail="Workflow execution failed.",
        ) from exc


@router.get("/workflows")
async def get_workflows():
    return {"workflows": workflow_store.list_all()}


@router.get("/workflows/{workflow_id}/state")
async def get_workflow_state(
    workflow_id: str,
):
    config = {
        "configurable": {
            "thread_id": workflow_id,
        },
    }

    try:
        state = workflow_app.get_state(config)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve workflow state.",
        ) from exc

    if state is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow state not found.",
        )

    return {
        "workflow_id": workflow_id,
        "values": state.values,
        "next": list(state.next),
        "tasks": [
            {
                "name": task.name,
                "id": task.id,
            }
            for task in state.tasks
        ],
        "interrupts": [
            str(interrupt)
            for interrupt in state.interrupts
        ],
    }


@router.get("/workflows/{workflow_id}", response_model=WorkflowStatusResponse)
def workflow_status(workflow_id: str) -> WorkflowStatusResponse:
    record = workflow_store.get(workflow_id)

    if not record:
        raise HTTPException(status_code=404, detail="Workflow not found.")

    return WorkflowStatusResponse(
        workflow_id=record["workflow_id"],
        request_id=record["request_id"],
        status=record["status"],
        intent=record["intent"],
        selected_agent=record["selected_agent"],
        confidence=record.get("confidence", 0.0),
        routing_source=record.get("routing_source", "unknown"),
        routing_reason=record.get("routing_reason", ""),
        iteration_count=record["iteration_count"],
        response=record["response"],
        error=record.get("error"),
    )
