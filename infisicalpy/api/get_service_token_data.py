from infisicalpy.api.models import GetServiceTokenDetailsResponse
from infisicalpy.utils.http import BaseUrlSession


def get_service_token_data(
    api_request: BaseUrlSession,
) -> GetServiceTokenDetailsResponse:
    response = api_request.get("/api/v2/service-token")

    return GetServiceTokenDetailsResponse.parse_obj(response.json())
