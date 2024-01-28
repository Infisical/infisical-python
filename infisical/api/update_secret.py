from infisical.models.api import SecretResponse, UpdateSecretDTO
from requests import Session


def update_secret_req(api_request: Session, options: UpdateSecretDTO) -> SecretResponse:
    response = api_request.patch(
        url=f"/api/v3/secrets/{options.secret_name}",
        json={
            "workspaceId": options.workspace_id,
            "environment": options.environment,
            "type": options.type,
            "secretValueCiphertext": options.secret_value_ciphertext,
            "secretValueIV": options.secret_value_iv,
            "secretValueTag": options.secret_value_tag,
            "secretPath": options.path,
        },
    )

    json_object = response.json()

    json_object["secret"]["workspace"] = options.workspace_id
    json_object["secret"]["environment"] = options.environment

    return SecretResponse.parse_obj(json_object)
