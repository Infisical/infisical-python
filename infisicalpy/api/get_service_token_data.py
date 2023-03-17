from infisicalpy.api.models import GetServiceTokenDetailsResponse
from requests import Session


def get_service_token_data(
    api_request: Session,
) -> GetServiceTokenDetailsResponse:
    """Send request again Infisical API to fetch service token data.
    See more information on https://infisical.com/docs/api-reference/endpoints/service-tokens/get

    :param api_request: The :class:`requests.Session` instance used to perform the request
    :return: Returns the API response as-is
    """
    response = api_request.get("/api/v2/service-token")

    return GetServiceTokenDetailsResponse.parse_obj(response.json())
