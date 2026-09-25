import boto3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.config.settings import get_settings


def main():

    settings = get_settings()

    session = boto3.Session(
        profile_name=settings.aws_profile,
    )

    dynamodb = session.resource(
        "dynamodb",
        region_name=settings.aws_region,
    )

    existing_tables = dynamodb.meta.client.list_tables(
    )["TableNames"]

    if settings.dynamodb_table_name in existing_tables:

        print(
            f"Table already exists: "
            f"{settings.dynamodb_table_name}"
        )

        return

    table = dynamodb.create_table(
        TableName=settings.dynamodb_table_name,

        KeySchema=[
            {
                "AttributeName": "ticket_id",
                "KeyType": "HASH",
            }
        ],

        AttributeDefinitions=[
            {
                "AttributeName": "ticket_id",
                "AttributeType": "S",
            }
        ],

        BillingMode="PAY_PER_REQUEST",
    )

    print(
        f"Created DynamoDB table: "
        f"{table.table_name}"
    )

    table.wait_until_exists()

    print("DynamoDB table is ready.")


if __name__ == "__main__":
    main()