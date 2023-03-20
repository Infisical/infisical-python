from infisical.api.models import GetEncryptedSecretsV2Response
from requests import Session


def get_secrets(
    api_request: Session, workspace_id: str, environment: str
) -> GetEncryptedSecretsV2Response:
    """Send request again Infisical API to fetch secrets.
    See more information on https://infisical.com/docs/api-reference/endpoints/secrets/read

    :param api_request: The :class:`requests.Session` instance used to perform the request
    :param workspace_id: The ID of the workspace
    :param environment: The environment
    :return: Returns the API response as-is
    """
    response = api_request.get(
        "/api/v2/secrets",
        params={
            "environment": environment,
            "workspaceId": workspace_id,
            "tagSlugs": "",
        },
    )

    return GetEncryptedSecretsV2Response.parse_obj(response.json())
