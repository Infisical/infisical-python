from infisicalpy import __version__
from infisicalpy.utils.http import BaseUrlSession, get_http_client

USER_AGENT = f"InfisicalPythonSDK/{__version__}"


def create_api_request_with_auth(base_url: str, service_token: str) -> BaseUrlSession:
    api_request = get_http_client(base_url=base_url.rstrip("/"))

    api_request.headers.update({"User-Agent": USER_AGENT})
    api_request.headers.update({"Content-Type": "application/json"})
    api_request.headers.update({"Authorization": f"Bearer {service_token}"})

    return api_request
