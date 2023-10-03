from typing import List, Tuple

from infisical.models.api import GetSecretsDTO, SecretImport, SecretsResponse
from infisical.models.models import Secret
from requests import Session


def get_secrets_req(
    api_request: Session, options: GetSecretsDTO
) -> Tuple[List[Secret], List[SecretImport]]:
    """Send request again Infisical API to fetch secrets.
    See more information on https://infisical.com/docs/api-reference/endpoints/secrets/read

    :param api_request: The :class:`requests.Session` instance used to perform the request
    :param workspace_id: The ID of the workspace
    :param environment: The environment
    :return: Returns the API response as-is
    """

    response = api_request.get(
        "/api/v3/secrets",
        params={
            "environment": options.environment,
            "workspaceId": options.workspace_id,
            "secretPath": options.path,
            "include_imports": str(options.include_imports).lower(),
        },
    )
    data = SecretsResponse.model_validate_json(response.text)

    return (data.secrets if data.secrets else [], data.imports if data.imports else [])
