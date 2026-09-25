from datetime import datetime, timezone
from uuid import uuid4


def create_request_id() -> str:
    """Create a human-readable request identifier."""
    date_part = datetime.now(timezone.utc).strftime("%Y%m%d")
    short_id = uuid4().hex[:8].upper()
    return f"EF-{date_part}-{short_id}"


def create_workflow_id() -> str:
    """Create a workflow identifier."""
    return f"WF-{uuid4().hex[:12].upper()}"


def generate_request_id() -> str:
    """Backward-compatible alias for request id generation."""
    return create_request_id()


def generate_workflow_id() -> str:
    """Backward-compatible alias for workflow id generation."""
    return create_workflow_id()