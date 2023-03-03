from infisicalpy.api.models import (
    GetEncryptedSecretsV2Request,
    GetEncryptedSecretsV2Response,
    GetServiceTokenDetailsResponse,
)
from requests import Session

USER_AGENT = "infisicalpy"


def call_get_service_token_details_v2(
    http_client: Session, api_url: str
) -> GetServiceTokenDetailsResponse:
    http_client.headers.update({"User-Agent": USER_AGENT})

    response = http_client.get(f"{api_url}/v2/service-token")

    return GetServiceTokenDetailsResponse.parse_obj(response.json())


def call_get_secrets_v2(
    http_client: Session, api_url: str, request: GetEncryptedSecretsV2Request
) -> GetEncryptedSecretsV2Response:
    http_client.headers.update({"User-Agent": USER_AGENT})

    response = http_client.get(
        f"{api_url}/v2/secrets",
        params={
            "environment": request.environment,
            "workspaceId": request.workspace_id,
            "tagSlugs": request.tag_slugs,
        },
    )

    return GetEncryptedSecretsV2Response.parse_obj(response.json())
