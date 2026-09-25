from datetime import datetime, timezone
from typing import Any

from backend.app.config.settings import get_settings
from backend.app.services.aws_clients import (
    get_dynamodb_resource,
)


class DynamoDBTicketStore:

    def __init__(self):
        settings = get_settings()

        self.table_name = settings.dynamodb_table_name

        self.dynamodb = get_dynamodb_resource()

        self.table = self.dynamodb.Table(
            self.table_name
        )

    def create_ticket(
        self,
        *,
        ticket_id: str,
        user_id: str,
        summary: str,
    ) -> dict[str, Any]:

        ticket = {
            "ticket_id": ticket_id,
            "user_id": user_id,
            "summary": summary,
            "status": "OPEN",
            "created_at": datetime.now(
                timezone.utc
            ).isoformat(),
        }

        self.table.put_item(
            Item=ticket
        )

        return ticket

    def get_ticket(
        self,
        ticket_id: str,
    ) -> dict[str, Any] | None:

        response = self.table.get_item(
            Key={
                "ticket_id": ticket_id
            }
        )

        return response.get("Item")