from infisicalpy import __version__
from infisicalpy.utils.http import BaseUrlSession, get_http_client

from .get_secrets import get_secrets as get_secrets
from .get_service_token_data import get_service_token_data as get_service_token_data

USER_AGENT = f"InfisicalPythonSDK/{__version__}"


def create_api_request_with_auth(base_url: str, service_token: str) -> BaseUrlSession:
    api_request = get_http_client(base_url=base_url)

    api_request.headers.update({"User-Agent": USER_AGENT})
    api_request.headers.update({"Content-Type": "application/json"})
    api_request.headers.update({"Authorization": f"Bearer {service_token}"})

    return api_request
