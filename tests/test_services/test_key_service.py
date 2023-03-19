from infisicalpy.api.models import GetEncryptedSecretsV2Response
from infisicalpy.services.key_service import KeyService

from tests.data.secrets_reponse import JSON_SECRETS_ENCRYPTED


def test_decrypt_secrets() -> None:
    secrets = KeyService.decrypt_secrets(
        workspace_key="9c07298c06c6aaa762fcee342cf6bc34".encode("utf-8"),
        encrypted_secrets=GetEncryptedSecretsV2Response.parse_obj(
            JSON_SECRETS_ENCRYPTED
        ).secrets,
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
