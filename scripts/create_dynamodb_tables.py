import sys
from pathlib import Path

import boto3

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.config.settings import get_settings


def _existing_tables(dynamodb) -> set[str]:
    return set(dynamodb.list_tables(Limit=100).get("TableNames", []))


def create_ticket_table(dynamodb, table_name: str) -> None:
    if table_name in _existing_tables(dynamodb):
        print(f"Ticket table already exists: {table_name}")
        return

    print(f"Creating ticket table: {table_name}")
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "ticket_id", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "ticket_id", "AttributeType": "S"}
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    print("Ticket table creation requested.")


def create_workflow_table(dynamodb, table_name: str) -> None:
    if table_name in _existing_tables(dynamodb):
        print(f"Workflow table already exists: {table_name}")
        return

    print(f"Creating workflow table: {table_name}")
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "workflow_id", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "workflow_id", "AttributeType": "S"}
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    print("Workflow table creation requested.")


def create_approval_table(dynamodb, table_name: str) -> None:
    if table_name in _existing_tables(dynamodb):
        print(f"Approval table already exists: {table_name}")
        return

    print(f"Creating approval table: {table_name}")
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "approval_id", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "approval_id", "AttributeType": "S"},
            {"AttributeName": "workflow_id", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "workflow_id-index",
                "KeySchema": [
                    {"AttributeName": "workflow_id", "KeyType": "HASH"}
                ],
                "Projection": {"ProjectionType": "ALL"},
            }
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    print("Approval table creation requested.")


def main() -> None:
    settings = get_settings()

    session_kwargs = {"region_name": settings.aws_region}
    if settings.aws_profile:
        session_kwargs["profile_name"] = settings.aws_profile

    session = boto3.Session(**session_kwargs)
    dynamodb = session.client("dynamodb")

    create_ticket_table(dynamodb, settings.dynamodb_table_name)
    create_workflow_table(
        dynamodb,
        settings.dynamodb_workflow_table_name,
    )
    create_approval_table(
        dynamodb,
        settings.dynamodb_approval_table_name,
    )


if __name__ == "__main__":
    main()
