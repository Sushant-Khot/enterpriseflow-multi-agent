from datetime import datetime, timezone
from typing import Any

from backend.app.config.settings import get_settings


class InMemoryWorkflowStore:
    def __init__(self) -> None:
        self._workflows: dict[str, dict[str, Any]] = {}

    def create(
        self,
        workflow_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        workflow = {
            "workflow_id": workflow_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            **data,
        }

        self._workflows[workflow_id] = workflow
        return workflow

    def update(
        self,
        workflow_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any] | None:
        if workflow_id not in self._workflows:
            return None

        self._workflows[workflow_id].update(data)
        self._workflows[workflow_id]["updated_at"] = (
            datetime.now(timezone.utc).isoformat()
        )

        return self._workflows[workflow_id]

    def get(
        self,
        workflow_id: str,
    ) -> dict[str, Any] | None:
        return self._workflows.get(workflow_id)

    def list_all(self) -> list[dict[str, Any]]:
        workflows = list(self._workflows.values())
        workflows.sort(
            key=lambda item: item.get("created_at", ""),
            reverse=True,
        )
        return workflows

    def save(
        self,
        workflow_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """Backward-compatible alias for the legacy store API."""
        return self.create(workflow_id, data)


class WorkflowStore:
    def __init__(self) -> None:
        settings = get_settings()
        self.use_dynamodb = settings.dynamodb_enabled
        self._memory = InMemoryWorkflowStore()
        self._dynamodb = None

        if self.use_dynamodb:
            from backend.app.services.dynamodb_workflow_store import (
                DynamoDBWorkflowStore,
            )

            self._dynamodb = DynamoDBWorkflowStore()

    def create(
        self,
        workflow_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        if self._dynamodb:
            return self._dynamodb.create(workflow_id, data)

        return self._memory.create(workflow_id, data)

    def save(
        self,
        workflow_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """Backward-compatible alias for the legacy store API."""
        return self.create(workflow_id, data)

    def update(
        self,
        workflow_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any] | None:
        if self._dynamodb:
            return self._dynamodb.update(workflow_id, data)

        return self._memory.update(workflow_id, data)

    def get(
        self,
        workflow_id: str,
    ) -> dict[str, Any] | None:
        if self._dynamodb:
            return self._dynamodb.get(workflow_id)

        return self._memory.get(workflow_id)

    def list_all(self) -> list[dict[str, Any]]:
        if self._dynamodb:
            return self._dynamodb.list_all()

        return self._memory.list_all()


workflow_store = WorkflowStore()
