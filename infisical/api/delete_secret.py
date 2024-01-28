from infisical.models.api import DeleteSecretDTO, SecretResponse
from requests import Session


def delete_secret_req(api_request: Session, options: DeleteSecretDTO) -> SecretResponse:
    response = api_request.delete(
        url=f"/api/v3/secrets/{options.secret_name}",
        json={
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
