from infisical.models.api import CreateSecretDTO, SecretResponse
from requests import Session


def create_secret_req(api_request: Session, options: CreateSecretDTO) -> SecretResponse:
    response = api_request.post(
        url=f"/api/v3/secrets/{options.secret_name}",
        json={
            "workspaceId": options.workspace_id,
            "environment": options.environment,
            "type": options.type,
            "secretKeyCiphertext": options.secret_key_ciphertext,
            "secretKeyIV": options.secret_key_iv,
            "secretKeyTag": options.secret_key_tag,
            "secretValueCiphertext": options.secret_value_ciphertext,
            "secretValueIV": options.secret_value_iv,
            "secretValueTag": options.secret_value_tag,
            "secretPath": options.path,
        },
    )

    return SecretResponse.parse_obj(response.json())
