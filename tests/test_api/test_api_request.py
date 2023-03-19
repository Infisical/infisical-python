from infisicalpy.__version__ import __version__
from infisicalpy.api import create_api_request_with_auth


def test_create_api_request() -> None:
    session = create_api_request_with_auth(
        base_url="https://test.infisical.local", service_token="123"
    )

    assert session.base_url == "https://test.infisical.local"
    assert session.headers["User-Agent"] == f"InfisicalPythonSDK/{__version__}"
    assert session.headers["Authorization"] == "Bearer 123"

    session = create_api_request_with_auth(
        base_url="https://test.infisical.local/", service_token="123"
    )

    assert session.base_url == "https://test.infisical.local"
