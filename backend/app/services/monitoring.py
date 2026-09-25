import logging

from backend.app.config.settings import get_settings
from backend.app.services.aws_clients import (
    get_cloudwatch_client,
)


logger = logging.getLogger(__name__)


def record_metric(
    metric_name: str,
    value: float = 1.0,
):
    settings = get_settings()

    if not settings.cloudwatch_metrics_enabled:
        return

    try:

        cloudwatch = get_cloudwatch_client()

        cloudwatch.put_metric_data(
            Namespace=settings.cloudwatch_namespace,

            MetricData=[
                {
                    "MetricName": metric_name,
                    "Value": value,
                    "Unit": "Count",
                }
            ],
        )

    except Exception:

        # Monitoring failure must not
        # break the application.

        logger.exception(
            "CloudWatch metric failed: %s",
            metric_name,
        )