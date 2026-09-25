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

    def list_tickets(self) -> list[dict[str, Any]]:
        response = self.table.scan()
        return response.get("Items", [])

    def update_ticket(
        self,
        ticket_id: str,
        *,
        status: str | None = None,
        summary: str | None = None,
    ) -> dict[str, Any] | None:
        ticket = self.get_ticket(ticket_id)

        if ticket is None:
            return None

        if status is not None:
            ticket["status"] = status

        if summary is not None:
            ticket["summary"] = summary

        ticket["updated_at"] = datetime.now(
            timezone.utc
        ).isoformat()

        self.table.put_item(Item=ticket)
        return ticket