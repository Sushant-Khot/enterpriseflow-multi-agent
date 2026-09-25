import logging
from functools import lru_cache
from typing import Any

from langchain_aws import ChatBedrockConverse

from backend.app.config.settings import get_settings

logger = logging.getLogger(__name__)


def _extract_text(content: Any) -> str:
    """
    Normalize LangChain AIMessage content into plain text.
    """

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts: list[str] = []

        for block in content:
            if isinstance(block, dict):
                text = block.get("text")

                if isinstance(text, str):
                    text_parts.append(text)

        return "".join(text_parts)

    return str(content)


@lru_cache
def get_bedrock_model() -> ChatBedrockConverse:
    """
    Create one reusable Bedrock model instance.

    Credentials are intentionally NOT stored in application code.
    LangChain/Boto3 uses the standard AWS credential chain.
    """

    settings = get_settings()

    if not settings.bedrock_enabled:
        raise RuntimeError(
            "Amazon Bedrock is disabled. "
            "Set BEDROCK_ENABLED=true in .env."
        )

    kwargs = {
        "model": settings.bedrock_model_id,
        "region_name": settings.aws_region,
        "temperature": settings.bedrock_temperature,
        "max_tokens": settings.bedrock_max_tokens,
        "max_retries": settings.bedrock_max_retries,
    }

    if settings.aws_profile:
        kwargs["credentials_profile_name"] = settings.aws_profile

    logger.info(
        "Initializing Bedrock model: %s",
        settings.bedrock_model_id,
    )

    return ChatBedrockConverse(**kwargs)


def invoke_bedrock(
    system_prompt: str,
    user_prompt: str,
) -> dict[str, Any]:
    """
    Invoke Amazon Bedrock using LangChain's ChatBedrockConverse.

    Returns both the generated text and usage metadata.
    """

    model = get_bedrock_model()

    response = model.invoke(
        [
            ("system", system_prompt),
            ("human", user_prompt),
        ]
    )

    text = _extract_text(response.content)

    usage = getattr(
        response,
        "usage_metadata",
        {},
    ) or {}

    metadata = getattr(
        response,
        "response_metadata",
        {},
    ) or {}

    return {
        "text": text,
        "usage": usage,
        "metadata": metadata,
    }