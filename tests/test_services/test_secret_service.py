import responses
from infisicalpy.api import create_api_request_with_auth
from infisicalpy.services.secret_service import SecretService

from tests.data.secrets_reponse import GET_SECRETS_RESPONSE
from tests.data.service_token import BEARER_TOKEN, GET_SERVICE_TOKEN_RESPONSE


@responses.activate
def test_get_decrypted_details() -> None:
    responses.add(GET_SERVICE_TOKEN_RESPONSE)
    responses.add(GET_SECRETS_RESPONSE)

    session = create_api_request_with_auth(
        base_url="https://test.infisical.local", service_token=BEARER_TOKEN
    )

    secrets, token_details = SecretService.get_decrypted_details(
        session, "0b305d2a033617cdc2d737d34a4b9dd1".encode("utf-8")
    )

    assert len(secrets) == 7
    assert secrets[0].key == "DATABASE_URL"
    assert secrets[0].value == "mongodb+srv://${DB_USERNAME}:${DB_PASSWORD}@mongodb.net"
    assert secrets[0].type == "shared"
    assert secrets[1].key == "DB_USERNAME"
    assert secrets[1].value == "OVERRIDE_THIS"
    assert secrets[1].type == "shared"
    assert secrets[2].key == "DB_PASSWORD"
    assert secrets[2].value == "OVERRIDE_THIS"
    assert secrets[2].type == "shared"
    assert secrets[3].key == "TWILIO_AUTH_TOKEN"
    assert secrets[3].value == "example_twillio_token"
    assert secrets[3].type == "shared"
    assert secrets[4].key == "WEBSITE_URL"
    assert secrets[4].value == "http://localhost:3000"
    assert secrets[4].type == "shared"
    assert secrets[5].key == "DB_USERNAME"
    assert secrets[5].value == "user1234"
    assert secrets[5].type == "personal"
    assert secrets[6].key == "DB_PASSWORD"
    assert secrets[6].value == "example_password"
    assert secrets[6].type == "personal"

    assert token_details.environment == "dev"
    assert token_details.workspace == "6af866f8a76030530fb57a1f"
