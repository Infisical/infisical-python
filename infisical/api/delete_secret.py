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

    return SecretResponse.model_validate_json(response.text)
