from infisical.api.models import GetServiceTokenKeyResponse
from requests import Session


def get_service_token_data_key_req(
    api_request: Session,
) -> GetServiceTokenKeyResponse:
    """Send request again Infisical API to fetch service token data v3 key.

    :param api_request: The :class:`requests.Session` instance used to perform the request
    :return: Returns the API response as-is
    """
    response = api_request.get("/api/v3/service-token/me/key")

    return GetServiceTokenKeyResponse.parse_obj(response.json())
