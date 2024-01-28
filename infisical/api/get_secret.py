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

    json_object = response.json()

    json_object["secret"]["workspace"] = options.workspace_id
    json_object["secret"]["environment"] = options.environment

    return SecretResponse.parse_obj(json_object)
