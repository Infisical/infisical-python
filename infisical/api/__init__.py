from infisical.__version__ import __version__
from infisical.utils.http import BaseUrlSession, get_http_client

USER_AGENT = f"InfisicalPythonSDK/{__version__}"


def create_api_request_with_auth(base_url: str, service_token: str) -> BaseUrlSession:
    """Returns a :class:`requests.Session` with a ``base_url`` and the authorization
    bearer set to the ``service_token``.

    :param base_url: The base url to use
    :param service_token: The service token to use as a authorization bearer token
    :return: A :class:`requests.Session` instance preconfigured
    """
    api_request = get_http_client(base_url=base_url.rstrip("/"))

    api_request.headers.update({"User-Agent": USER_AGENT})
    api_request.headers.update({"Content-Type": "application/json"})
    api_request.headers.update({"Authorization": f"Bearer {service_token}"})

    return api_request
