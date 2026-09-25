import sys
from pathlib import Path

import boto3

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.config.settings import get_settings


def main() -> None:
    settings = get_settings()

    if settings.aws_profile:
        session = boto3.Session(
            profile_name=settings.aws_profile,
            region_name=settings.aws_region,
        )
    else:
        session = boto3.Session(
            region_name=settings.aws_region,
        )

    dynamodb = session.client("dynamodb")
    table_name = settings.langgraph_checkpoint_table_name
    existing_tables = dynamodb.list_tables(Limit=100)["TableNames"]

    if table_name in existing_tables:
        print(f"Checkpoint table already exists: {table_name}")
        return

    print(f"Creating checkpoint table: {table_name}")

    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                "AttributeName": "PK",
                "KeyType": "HASH",
            },
            {
                "AttributeName": "SK",
                "KeyType": "RANGE",
            },
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "PK",
                "AttributeType": "S",
            },
            {
                "AttributeName": "SK",
                "AttributeType": "S",
            },
        ],
        BillingMode="PAY_PER_REQUEST",
    )

    print("Checkpoint table creation requested.")


if __name__ == "__main__":
    main()