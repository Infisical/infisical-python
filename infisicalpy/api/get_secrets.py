from infisicalpy.api.models import GetEncryptedSecretsV2Response
from infisicalpy.utils.http import BaseUrlSession


def get_secrets(
    api_request: BaseUrlSession, workspace_id: str, environment: str
) -> GetEncryptedSecretsV2Response:
    response = api_request.get(
        "/api/v2/secrets",
        params={
            "environment": environment,
            "workspaceId": workspace_id,
            "tagSlugs": "",
        },
    )

    return GetEncryptedSecretsV2Response.parse_obj(response.json())
