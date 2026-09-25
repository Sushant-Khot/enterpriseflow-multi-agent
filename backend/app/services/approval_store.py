from datetime import datetime, timezone
from typing import Any
import uuid

from backend.app.config.settings import get_settings


class InMemoryApprovalStore:
    def __init__(self) -> None:
        self._approvals: dict[str, dict[str, Any]] = {}

    def create_approval(
        self,
        workflow_id: str,
        review: str,
    ) -> dict[str, Any]:
        existing = self.get_by_workflow(workflow_id)

        if existing:
            return existing

        approval_id = f"APR-{uuid.uuid4().hex[:10].upper()}"
        now = datetime.now(timezone.utc).isoformat()
        approval = {
            "approval_id": approval_id,
            "workflow_id": workflow_id,
            "status": "PENDING",
            "review": review,
            "feedback": "",
            "approved": None,
            "created_at": now,
            "updated_at": now,
        }

        self._approvals[approval_id] = approval
        return approval

    def get(
        self,
        approval_id: str,
    ) -> dict[str, Any] | None:
        return self._approvals.get(approval_id)

    def get_by_workflow(
        self,
        workflow_id: str,
    ) -> dict[str, Any] | None:
        for approval in self._approvals.values():
            if approval["workflow_id"] == workflow_id:
                return approval

        return None

    def submit_feedback(
        self,
        approval_id: str,
        approved: bool,
        feedback: str = "",
    ) -> dict[str, Any]:
        approval = self.get(approval_id)

        if approval is None:
            raise ValueError("Approval not found.")

        if approval["status"] != "PENDING":
            raise ValueError("This approval has already been processed.")

        approval["approved"] = approved
        approval["feedback"] = feedback
        approval["status"] = "APPROVED" if approved else "REVISION_REQUESTED"
        approval["updated_at"] = datetime.now(timezone.utc).isoformat()
        return approval


class ApprovalStore:
    def __init__(self) -> None:
        settings = get_settings()
        self.use_dynamodb = settings.dynamodb_enabled
        self._memory = InMemoryApprovalStore()
        self._dynamodb = None

        if self.use_dynamodb:
            from backend.app.services.dynamodb_approval_store import (
                DynamoDBApprovalStore,
            )

            self._dynamodb = DynamoDBApprovalStore()

    def create_approval(
        self,
        workflow_id: str,
        review: str,
    ) -> dict[str, Any]:
        if self._dynamodb:
            return self._dynamodb.create_approval(workflow_id, review)

        return self._memory.create_approval(workflow_id, review)

    def get(
        self,
        approval_id: str,
    ) -> dict[str, Any] | None:
        if self._dynamodb:
            return self._dynamodb.get(approval_id)

        return self._memory.get(approval_id)

    def get_by_workflow(
        self,
        workflow_id: str,
    ) -> dict[str, Any] | None:
        if self._dynamodb:
            return self._dynamodb.get_by_workflow(workflow_id)

        return self._memory.get_by_workflow(workflow_id)

    def submit_feedback(
        self,
        approval_id: str,
        approved: bool,
        feedback: str = "",
    ) -> dict[str, Any]:
        if self._dynamodb:
            return self._dynamodb.submit_feedback(
                approval_id,
                approved,
                feedback,
            )

        return self._memory.submit_feedback(
            approval_id,
            approved,
            feedback,
        )


approval_store = ApprovalStore()
