from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application configuration."""

    app_name: str = Field(
        default="EnterpriseFlow AI",
        alias="APP_NAME",
    )

    app_env: str = Field(
        default="development",
        alias="APP_ENV",
    )

    app_version: str = Field(
        default="0.2.0",
        alias="APP_VERSION",
    )

    log_level: str = Field(
        default="INFO",
        alias="LOG_LEVEL",
    )

    api_prefix: str = Field(
        default="/api/v1",
        alias="API_PREFIX",
    )

    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        alias="CORS_ORIGINS",
    )

    # -----------------------------
    # AWS
    # -----------------------------

    aws_region: str = Field(
        default="us-east-1",
        alias="AWS_REGION",
    )

    aws_profile: str = Field(
        default="",
        alias="AWS_PROFILE",
    )

    # -----------------------------
    # Amazon Bedrock
    # -----------------------------

    bedrock_enabled: bool = Field(
        default=False,
        alias="BEDROCK_ENABLED",
    )

    bedrock_model_id: str = Field(
        default="amazon.nova-micro-v1:0",
        alias="BEDROCK_MODEL_ID",
    )

    bedrock_max_tokens: int = Field(
        default=200,
        alias="BEDROCK_MAX_TOKENS",
    )

    bedrock_temperature: float = Field(
        default=0.0,
        alias="BEDROCK_TEMPERATURE",
    )

    bedrock_max_retries: int = Field(
        default=2,
        alias="BEDROCK_MAX_RETRIES",
    )

    guardrails_enabled: bool = Field(
        default=False,
        alias="GUARDRAILS_ENABLED",
    )

    bedrock_guardrail_id: str = Field(
        default="",
        alias="BEDROCK_GUARDRAIL_ID",
    )

    bedrock_guardrail_version: str = Field(
        default="DRAFT",
        alias="BEDROCK_GUARDRAIL_VERSION",
    )

    cloudwatch_metrics_enabled: bool = Field(
        default=False,
        alias="CLOUDWATCH_METRICS_ENABLED",
    )

    cloudwatch_namespace: str = Field(
        default="EnterpriseFlow",
        alias="CLOUDWATCH_NAMESPACE",
    )

    # -----------------------------
    # Agent controls
    # -----------------------------

    max_agent_iterations: int = Field(
        default=5,
        alias="MAX_AGENT_ITERATIONS",
    )

    workflow_ttl_seconds: int = Field(
        default=3600,
        alias="WORKFLOW_TTL_SECONDS",
    )

    # -----------------------------
    # DynamoDB
    # -----------------------------

    dynamodb_enabled: bool = Field(
        default=False,
        alias="DYNAMODB_ENABLED",
    )

    dynamodb_table_name: str = Field(
        default="enterpriseflow-tickets",
        alias="DYNAMODB_TABLE_NAME",
    )

    dynamodb_workflow_table_name: str = Field(
        default="enterpriseflow-workflows",
        alias="DYNAMODB_WORKFLOW_TABLE_NAME",
    )

    dynamodb_approval_table_name: str = Field(
        default="enterpriseflow-approvals",
        alias="DYNAMODB_APPROVAL_TABLE_NAME",
    )

    langgraph_checkpoint_enabled: bool = Field(
        default=False,
        alias="LANGGRAPH_CHECKPOINT_ENABLED",
    )

    langgraph_checkpoint_table_name: str = Field(
        default="enterpriseflow-langgraph-checkpoints",
        alias="LANGGRAPH_CHECKPOINT_TABLE_NAME",
    )

    langgraph_checkpoint_ttl_seconds: int = Field(
        default=2592000,
        alias="LANGGRAPH_CHECKPOINT_TTL_SECONDS",
    )
    
    # -----------------------------
    # Amazon SQS
    # -----------------------------

    sqs_enabled: bool = Field(
        default=False,
        alias="SQS_ENABLED",
    )

    sqs_queue_url: str = Field(
        default="",
        alias="SQS_QUEUE_URL",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()