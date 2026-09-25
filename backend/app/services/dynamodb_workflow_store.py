from decimal import Decimal
from typing import Any

from backend.app.config.settings import get_settings
from backend.app.services.aws_clients import (
    get_dynamodb_resource,
)


def _to_dynamodb(value: Any):

    if isinstance(value, float):
        return Decimal(str(value))

    if isinstance(value, dict):
        return {
            key: _to_dynamodb(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            _to_dynamodb(item)
            for item in value
        ]

    return value


def _from_dynamodb(value: Any):

    if isinstance(value, Decimal):

        if value == value.to_integral_value():
            return int(value)

        return float(value)

    if isinstance(value, dict):
        return {
            key: _from_dynamodb(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            _from_dynamodb(item)
            for item in value
        ]

    return value


class DynamoDBWorkflowStore:

    def __init__(self):

        settings = get_settings()

        self.table_name = (
            settings.dynamodb_workflow_table_name
        )

        self.table = (
            get_dynamodb_resource()
            .Table(self.table_name)
        )


    def create(
        self,
        workflow_id: str,
        data: dict[str, Any],
    ):

        item = {
            "workflow_id": workflow_id,
            **data,
        }

        item = _to_dynamodb(item)

        self.table.put_item(
            Item=item
        )

        return _from_dynamodb(item)


    def update(
        self,
        workflow_id: str,
        data: dict[str, Any],
    ):

        existing = self.get(
            workflow_id
        )

        if existing is None:
            return None

        existing.update(data)

        return self.create(
            workflow_id,
            existing,
        )


    def get(
        self,
        workflow_id: str,
    ):

        response = self.table.get_item(
            Key={
                "workflow_id": workflow_id
            }
        )

        item = response.get("Item")

        if item is None:
            return None

        return _from_dynamodb(item)


    def list_all(self):

        response = self.table.scan()

        items = response.get(
            "Items",
            [],
        )

        workflows = [
            _from_dynamodb(item)
            for item in items
        ]

        workflows.sort(
            key=lambda item:
            item.get("created_at", ""),
            reverse=True,
        )

        return workflows