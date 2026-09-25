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

    def list_tickets(self) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._tickets.values())

    def update_ticket(
        self,
        ticket_id: str,
        *,
        status: str | None = None,
        summary: str | None = None,
    ) -> dict[str, Any] | None:
        with self._lock:
            ticket = self._tickets.get(ticket_id)

            if ticket is None:
                return None

            if status is not None:
                ticket["status"] = status

            if summary is not None:
                ticket["summary"] = summary

            ticket["updated_at"] = datetime.now(
                timezone.utc
            ).isoformat()

            return ticket


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

    def list_tickets(self) -> list[dict[str, Any]]:
        if self.dynamodb_store:
            return self.dynamodb_store.list_tickets()

        return self.local_store.list_tickets()

    def update_ticket(
        self,
        ticket_id: str,
        *,
        status: str | None = None,
        summary: str | None = None,
    ) -> dict[str, Any] | None:
        if self.dynamodb_store:
            return self.dynamodb_store.update_ticket(
                ticket_id,
                status=status,
                summary=summary,
            )

        return self.local_store.update_ticket(
            ticket_id,
            status=status,
            summary=summary,
        )


ticket_store = TicketStore()