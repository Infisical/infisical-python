from infisical.__version__ import __version__
from infisical.api import create_api_request_with_auth

from tests.data.service_token import BEARER_TOKEN


def test_create_api_request() -> None:
    session = create_api_request_with_auth(
        base_url="https://test.infisical.local", service_token=BEARER_TOKEN
    )

    assert session.base_url == "https://test.infisical.local"
    assert session.headers["User-Agent"] == f"InfisicalPythonSDK/{__version__}"
    assert session.headers["Authorization"] == f"Bearer {BEARER_TOKEN}"

    session = create_api_request_with_auth(
        base_url="https://test.infisical.local/", service_token=BEARER_TOKEN
    )

    assert session.base_url == "https://test.infisical.local"
