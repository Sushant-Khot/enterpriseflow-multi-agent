from functools import lru_cache
from typing import Any

from backend.app.config.settings import get_settings
from backend.app.services.aws_clients import get_boto3_session


@lru_cache
def get_bedrock_runtime_client():
    session = get_boto3_session()

    return session.client(
        "bedrock-runtime"
    )


def apply_guardrail(
    text: str,
    source: str,
) -> dict[str, Any]:

    settings = get_settings()

    if not settings.guardrails_enabled:
        return {
            "allowed": True,
            "action": "DISABLED",
            "text": text,
            "reason": "Guardrail disabled",
        }

    if not settings.bedrock_guardrail_id:
        raise RuntimeError(
            "BEDROCK_GUARDRAIL_ID is not configured."
        )

    if source not in {"INPUT", "OUTPUT"}:
        raise ValueError(
            "source must be INPUT or OUTPUT"
        )

    client = get_bedrock_runtime_client()

    response = client.apply_guardrail(
        guardrailIdentifier=(
            settings.bedrock_guardrail_id
        ),
        guardrailVersion=(
            settings.bedrock_guardrail_version
        ),
        source=source,
        content=[
            {
                "text": {
                    "text": text
                }
            }
        ],
        outputScope="FULL",
    )

    action = response.get(
        "action",
        "NONE"
    )

    outputs = response.get(
        "outputs",
        []
    )

    guarded_text = text

    if outputs:
        first_output = outputs[0]

        if isinstance(first_output, dict):
            guarded_text = first_output.get(
                "text",
                text
            )

    return {
        "allowed": action != "GUARDRAIL_INTERVENED",
        "action": action,
        "text": guarded_text,
        "reason": response.get(
            "actionReason",
            ""
        ),
        "assessments": response.get(
            "assessments",
            []
        ),
    }