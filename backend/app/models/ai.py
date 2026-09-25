from typing import Literal

from pydantic import BaseModel, Field


IntentType = Literal[
    "BLOG_REVIEW",
    "BACKGROUND_CHECK",
    "SALARY_INCENTIVE",
    "GENERAL_SUPPORT",
]


AgentType = Literal[
    "A1_BLOG",
    "A2_BACKGROUND",
    "A3_SALARY",
    "A4_SUPPORT",
]


class RoutingDecisionModel(BaseModel):
    """
    Validated output expected from the Bedrock orchestrator.
    """

    intent: IntentType = Field(
        description="The classified business intent."
    )

    agent: AgentType = Field(
        description="The specialist agent that should handle the request."
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1."
    )

    reason: str = Field(
        min_length=1,
        max_length=500,
        description="Short explanation for the routing decision."
    )