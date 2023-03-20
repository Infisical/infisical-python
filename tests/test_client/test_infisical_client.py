import pytest
import responses
from infisicalpy import InfisicalClient
from infisicalpy.exceptions import InfisicalTokenError

from tests.data.secrets_reponse import GET_SECRETS_RESPONSE
from tests.data.service_token import GET_SERVICE_TOKEN_RESPONSE, SERVICE_TOKEN


def test_init_empty_token() -> None:
    with pytest.raises(InfisicalTokenError):
        InfisicalClient(token="")


def test_init_toke_malformated() -> None:
    with pytest.raises(InfisicalTokenError):
        InfisicalClient(token="st.561qzd5")

    with pytest.raises(InfisicalTokenError):
        InfisicalClient(token="123")

    with pytest.raises(InfisicalTokenError):
        InfisicalClient(token="st.166.411")

    with pytest.raises(InfisicalTokenError):
        InfisicalClient(token="st.123456.123456.123456t")


@responses.activate
def test_setup_ok() -> None:
    responses.add(GET_SERVICE_TOKEN_RESPONSE)
    responses.add(GET_SECRETS_RESPONSE)

    client = InfisicalClient(
        token=SERVICE_TOKEN, site_url="https://test.infisical.local"
    )

    client.setup()

    assert len(client._secrets) == 5
    assert (
        client._secrets["DATABASE_URL"]
        == "mongodb+srv://${DB_USERNAME}:${DB_PASSWORD}@mongodb.net"
    )
    assert client._secrets["DB_USERNAME"] == "user1234"
    assert client._secrets["DB_PASSWORD"] == "example_password"
    assert client._secrets["TWILIO_AUTH_TOKEN"] == "example_twillio_token"
    assert client._secrets["WEBSITE_URL"] == "http://localhost:3000"


@responses.activate
def test_get_ok() -> None:
    responses.add(GET_SERVICE_TOKEN_RESPONSE)
    responses.add(GET_SECRETS_RESPONSE)

    client = InfisicalClient(
        token=SERVICE_TOKEN, site_url="https://test.infisical.local"
    )

    client.setup()

    assert client.get("TEST") is None
    assert (
        client.get("DATABASE_URL")
        == "mongodb+srv://${DB_USERNAME}:${DB_PASSWORD}@mongodb.net"
    )
    assert client.get("DB_USERNAME") == "user1234"
    assert client.get("DB_PASSWORD") == "example_password"
    assert client.get("TWILIO_AUTH_TOKEN") == "example_twillio_token"
    assert client.get("WEBSITE_URL") == "http://localhost:3000"
