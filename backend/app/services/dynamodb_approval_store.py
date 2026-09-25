from datetime import datetime, timezone
from decimal import Decimal
from typing import Any
import uuid

from backend.app.config.settings import get_settings
from backend.app.services.aws_clients import get_dynamodb_resource


def _to_dynamodb(value: Any) -> Any:
    if isinstance(value, float):
        return Decimal(str(value))

    if isinstance(value, dict):
        return {key: _to_dynamodb(item) for key, item in value.items()}

    if isinstance(value, list):
        return [_to_dynamodb(item) for item in value]

    return value


def _from_dynamodb(value: Any) -> Any:
    if isinstance(value, Decimal):
        if value == value.to_integral_value():
            return int(value)
        return float(value)

    if isinstance(value, dict):
        return {key: _from_dynamodb(item) for key, item in value.items()}

    if isinstance(value, list):
        return [_from_dynamodb(item) for item in value]

    return value


class DynamoDBApprovalStore:
    def __init__(self) -> None:
        settings = get_settings()
        self.table_name = settings.dynamodb_approval_table_name
        self.table = get_dynamodb_resource().Table(self.table_name)

    def create_approval(
        self,
        workflow_id: str,
        review: str,
    ) -> dict[str, Any]:
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

        self.table.put_item(Item=_to_dynamodb(approval))
        return approval

    def get(
        self,
        approval_id: str,
    ) -> dict[str, Any] | None:
        response = self.table.get_item(
            Key={"approval_id": approval_id}
        )
        item = response.get("Item")

        if item is None:
            return None

        return _from_dynamodb(item)

    def get_by_workflow(
        self,
        workflow_id: str,
    ) -> dict[str, Any] | None:
        response = self.table.query(
            IndexName="workflow_id-index",
            KeyConditionExpression="workflow_id = :workflow_id",
            ExpressionAttributeValues={":workflow_id": workflow_id},
            Limit=1,
        )
        items = response.get("Items", [])

        if not items:
            return None

        return _from_dynamodb(items[0])

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

        new_status = "APPROVED" if approved else "REVISION_REQUESTED"
        self.table.update_item(
            Key={"approval_id": approval_id},
            UpdateExpression=(
                "SET #status = :status, feedback = :feedback, "
                "approved = :approved, updated_at = :updated_at"
            ),
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={
                ":status": new_status,
                ":feedback": feedback,
                ":approved": approved,
                ":updated_at": datetime.now(timezone.utc).isoformat(),
            },
            ReturnValues="ALL_NEW",
        )

        return self.get(approval_id)
