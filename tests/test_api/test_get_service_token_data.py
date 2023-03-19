import responses
from infisicalpy.api import create_api_request_with_auth
from infisicalpy.api.get_service_token_data import get_service_token_data

from tests.data.service_token import GET_SERVICE_TOKEN_RESPONSE


@responses.activate
def test_get_secrets_correct() -> None:
    responses.add(GET_SERVICE_TOKEN_RESPONSE)

    session = create_api_request_with_auth(
        base_url="https://test.infisical.local", service_token="456"
    )

    service_token_data = get_service_token_data(session)

    assert (
        service_token_data.encrypted_key
        == "0C200uuKrhqQmc5kvzHrhSlPLxFkMwMy6eSD7dx+zxc="
    )
