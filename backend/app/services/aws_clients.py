import boto3

from functools import lru_cache

from backend.app.config.settings import get_settings


@lru_cache
def get_boto3_session():

    settings = get_settings()

    if settings.aws_profile:

        return boto3.Session(
            profile_name=settings.aws_profile,
            region_name=settings.aws_region,
        )

    return boto3.Session(
        region_name=settings.aws_region,
    )


@lru_cache
def get_dynamodb_resource():

    return get_boto3_session().resource(
        "dynamodb"
    )


@lru_cache
def get_dynamodb_client():

    return get_boto3_session().client(
        "dynamodb"
    )


@lru_cache
def get_sqs_client():

    return get_boto3_session().client(
        "sqs"
    )


@lru_cache
def get_cloudwatch_client():

    return get_boto3_session().client(
        "cloudwatch"
    )