import logging
from typing import Any

from backend.app.graph.state import AgentState
from backend.app.services.bedrock import invoke_bedrock
from backend.app.services.ticket_store import ticket_store

logger = logging.getLogger(__name__)


SUPPORT_SYSTEM_PROMPT = """
You are the Support Ticket Agent for EnterpriseFlow AI.

Create a concise support-ticket summary from the user's request.

Rules:

- Do not solve the issue.
- Do not invent facts.
- Do not include unnecessary personal information.
- Keep the summary professional.
- Maximum 300 characters.
"""


def summarize_support_request(user_input: str) -> str:
    """
    Generate a concise ticket summary.
    """

    try:
        result = invoke_bedrock(
            system_prompt=SUPPORT_SYSTEM_PROMPT,
            user_prompt=f"""
Create a concise support ticket summary for:

<request>
{user_input}
</request>
""",
        )

        summary = result["text"].strip()

        if len(summary) > 300:
            summary = summary[:297] + "..."

        return summary

    except Exception as exc:
        logger.warning(
            "Support Bedrock summarization failed. Using fallback. Error=%s",
            exc,
        )

        summary = "Support request: " + user_input.strip()

        if len(summary) > 300:
            summary = summary[:297] + "..."

        return summary


def support_agent(state: AgentState) -> dict[str, Any]:
    """
    A4 Support Ticket Agent.
    """

    user_input = state.get("user_input", "").strip()
    user_id = state.get("user_id", "UNKNOWN")

    if not user_input:
        return {
            "response": "Unable to create a support ticket because the request is empty.",
            "status": "FAILED",
            "error": "Empty support request.",
        }

    summary = summarize_support_request(user_input)

    ticket = ticket_store.create_ticket(
        user_id=user_id,
        summary=summary,
    )

    response = (
        "Your request has been converted into a support ticket.\n\n"
        f"Ticket ID: {ticket['ticket_id']}\n"
        f"Status: {ticket['status']}\n"
        f"Summary: {ticket['summary']}"
    )

    logger.info(
        "A4 support ticket created: ticket_id=%s",
        ticket["ticket_id"],
    )

    return {
        "response": response,
        "status": "COMPLETED",
        "requires_human_approval": False,
        "tool_results": {
            "agent": "A4_SUPPORT",
            "ticket": ticket,
        },
    }