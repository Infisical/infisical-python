from infisical.models.api import GetSecretDTO, SecretResponse
from requests import Session


def get_secret_req(api_request: Session, options: GetSecretDTO) -> SecretResponse:
    response = api_request.get(
        url=f"/api/v3/secrets/{options.secret_name}",
        params={
            "workspaceId": options.workspace_id,
            "environment": options.environment,
            "type": options.type,
            "secretPath": options.path,
        },
    )

    return SecretResponse.parse_obj(response.json())
