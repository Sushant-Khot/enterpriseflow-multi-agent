import threading
import uuid

from datetime import datetime, timezone
from typing import Any

from backend.app.config.settings import get_settings


class InMemoryTicketStore:

    def __init__(self) -> None:

        self._tickets: dict[
            str,
            dict[str, Any],
        ] = {}

        self._lock = threading.Lock()

    def create_ticket(
        self,
        *,
        ticket_id: str | None = None,
        user_id: str,
        summary: str,
    ) -> dict[str, Any]:

        generated_ticket_id = ticket_id or (
            f"TKT-{uuid.uuid4().hex[:10].upper()}"
        )

        ticket = {
            "ticket_id": generated_ticket_id,
            "user_id": user_id,
            "summary": summary,
            "status": "OPEN",
            "created_at": datetime.now(
                timezone.utc
            ).isoformat(),
        }

        with self._lock:
            self._tickets[generated_ticket_id] = ticket

        return ticket

    def get_ticket(
        self,
        ticket_id: str,
    ) -> dict[str, Any] | None:

        with self._lock:
            return self._tickets.get(ticket_id)


class TicketStore:

    def __init__(self):

        settings = get_settings()

        self.enabled = (
            settings.dynamodb_enabled
        )

        self.local_store = (
            InMemoryTicketStore()
        )

        self.dynamodb_store = None

        if self.enabled:

            from backend.app.services.dynamodb_ticket_store import (
                DynamoDBTicketStore,
            )

            self.dynamodb_store = (
                DynamoDBTicketStore()
            )

    def create_ticket(
        self,
        *,
        user_id: str,
        summary: str,
    ) -> dict[str, Any]:

        ticket_id = (
            f"TKT-{uuid.uuid4().hex[:10].upper()}"
        )

        if self.dynamodb_store:

            return self.dynamodb_store.create_ticket(
                ticket_id=ticket_id,
                user_id=user_id,
                summary=summary,
            )

        return self.local_store.create_ticket(
            ticket_id=ticket_id,
            user_id=user_id,
            summary=summary,
        )

    def get_ticket(
        self,
        ticket_id: str,
    ) -> dict[str, Any] | None:

        if self.dynamodb_store:

            return self.dynamodb_store.get_ticket(
                ticket_id
            )

        return self.local_store.get_ticket(
            ticket_id
        )


ticket_store = TicketStore()