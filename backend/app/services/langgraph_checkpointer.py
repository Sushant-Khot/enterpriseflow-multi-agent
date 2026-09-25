from functools import lru_cache

from langgraph.checkpoint.memory import (
    InMemorySaver,
)

from langgraph_checkpoint_aws import (
    DynamoDBSaver,
)

from backend.app.config.settings import (
    get_settings,
)

from backend.app.services.aws_clients import (
    get_boto3_session,
)


@lru_cache
def get_checkpointer():

    settings = get_settings()

    if not settings.langgraph_checkpoint_enabled:

        return InMemorySaver()

    session = get_boto3_session()

    return DynamoDBSaver(
        table_name=(
            settings
            .langgraph_checkpoint_table_name
        ),
        session=session,
        ttl_seconds=(
            settings
            .langgraph_checkpoint_ttl_seconds
        ),
        enable_checkpoint_compression=True,
    )