import boto3
import json


REGION = "us-east-1"
PROFILE = "enterpriseflow"


def main():
    session = boto3.Session(
        profile_name=PROFILE,
        region_name=REGION,
    )

    client = session.client("bedrock")

    response = client.create_guardrail(
        name="EnterpriseFlow-Guardrail",

        description=(
            "Security guardrail for EnterpriseFlow AI "
            "multi-agent enterprise automation platform."
        ),

        blockedInputMessaging=(
            "Your request was blocked because it "
            "violated the EnterpriseFlow security policy."
        ),

        blockedOutputsMessaging=(
            "The generated response was blocked because "
            "it violated the EnterpriseFlow security policy."
        ),

        contentPolicyConfig={
            "filtersConfig": [
                {
                    "type": "PROMPT_ATTACK",
                    "inputStrength": "HIGH",
                    "outputStrength": "NONE",
                    "inputModalities": ["TEXT"],
                    "outputModalities": ["TEXT"],
                    "inputAction": "BLOCK",
                    "outputAction": "BLOCK",
                    "inputEnabled": True,
                    "outputEnabled": True,
                }
            ]
        },

        sensitiveInformationPolicyConfig={
            "piiEntitiesConfig": [
                {
                    "type": "EMAIL",
                    "action": "ANONYMIZE",
                    "inputAction": "ANONYMIZE",
                    "outputAction": "ANONYMIZE",
                    "inputEnabled": True,
                    "outputEnabled": True,
                },
                {
                    "type": "PHONE",
                    "action": "ANONYMIZE",
                    "inputAction": "ANONYMIZE",
                    "outputAction": "ANONYMIZE",
                    "inputEnabled": True,
                    "outputEnabled": True,
                },
                {
                    "type": "CREDIT_DEBIT_CARD_NUMBER",
                    "action": "BLOCK",
                    "inputAction": "BLOCK",
                    "outputAction": "BLOCK",
                    "inputEnabled": True,
                    "outputEnabled": True,
                },
                {
                    "type": "PASSWORD",
                    "action": "BLOCK",
                    "inputAction": "BLOCK",
                    "outputAction": "BLOCK",
                    "inputEnabled": True,
                    "outputEnabled": True,
                },
                {
                    "type": "AWS_ACCESS_KEY",
                    "action": "BLOCK",
                    "inputAction": "BLOCK",
                    "outputAction": "BLOCK",
                    "inputEnabled": True,
                    "outputEnabled": True,
                },
                {
                    "type": "AWS_SECRET_KEY",
                    "action": "BLOCK",
                    "inputAction": "BLOCK",
                    "outputAction": "BLOCK",
                    "inputEnabled": True,
                    "outputEnabled": True,
                },
            ]
        },

        tags=[
            {
                "key": "Project",
                "value": "EnterpriseFlow",
            },
            {
                "key": "Environment",
                "value": "StudentCapstone",
            },
        ],
    )

    print("\n====================================")
    print("Bedrock Guardrail Created")
    print("====================================")

    print(
        json.dumps(
            {
                "guardrailId": response["guardrailId"],
                "guardrailArn": response["guardrailArn"],
                "version": response["version"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()