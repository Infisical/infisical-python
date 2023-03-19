import responses
from infisicalpy.api import create_api_request_with_auth
from infisicalpy.api.get_secrets import get_secrets

from tests.data.secrets_reponse import GET_SECRETS_RESPONSE


@responses.activate
def test_get_secrets_correct() -> None:
    responses.add(GET_SECRETS_RESPONSE)

    session = create_api_request_with_auth(
        base_url="https://test.infisical.local", service_token="456"
    )

    secrets = get_secrets(
        session, workspace_id="6af866f8a76030530fb57a1f", environment="dev"
    )

    assert len(secrets.secrets) == 7
    assert len(secrets.secrets[0].tags) == 2
    assert secrets.secrets[0].id == "63ff66fae68fef382d8d4c30"
