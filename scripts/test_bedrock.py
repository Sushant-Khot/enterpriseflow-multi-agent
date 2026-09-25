import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.config.settings import get_settings
from backend.app.services.bedrock import invoke_bedrock


def main():

    settings = get_settings()

    print("=" * 60)
    print("EnterpriseFlow AI - Bedrock Connectivity Test")
    print("=" * 60)

    print(
        f"Region      : {settings.aws_region}"
    )

    print(
        f"Model       : {settings.bedrock_model_id}"
    )

    print(
        f"Enabled     : {settings.bedrock_enabled}"
    )

    print("=" * 60)

    if not settings.bedrock_enabled:
        print("\nBedrock is disabled in this environment.")
        print("Set BEDROCK_ENABLED=true and validate AWS access to run a live connectivity check.")
        return

    result = invoke_bedrock(
        system_prompt=(
            "You are a concise technical assistant. "
            "Answer in one sentence."
        ),
        user_prompt=(
            "What is Amazon Bedrock?"
        ),
    )

    print("\nMODEL RESPONSE:")
    print(result["text"])

    print("\nUSAGE:")
    print(result["usage"])

    print("\nMETADATA:")
    print(result["metadata"])

    print("\nBedrock connectivity test completed.")


if __name__ == "__main__":
    main()