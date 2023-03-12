from infisicalpy.api.models import (
    GetEncryptedSecretsV2Request,
    GetEncryptedSecretsV2Response,
)
from infisicalpy.utils.http import BaseUrlSession


def get_secrets(
    api_request: BaseUrlSession, request: GetEncryptedSecretsV2Request
) -> GetEncryptedSecretsV2Response:
    response = api_request.get(
        "/api/v2/secrets",
        params={
            "environment": request.environment,
            "workspaceId": request.workspace_id,
            "tagSlugs": request.tag_slugs,
        },
    )

    return GetEncryptedSecretsV2Response.parse_obj(response.json())
