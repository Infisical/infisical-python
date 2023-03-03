from os import environ

import pytest
from infisicalpy import SecretService


def test_secretservice_init_token_no_env_no_params() -> None:
    # token should be provided either by param or env variable
    with pytest.raises(ValueError) as excinfo:
        SecretService()
    assert "Cannot find infisical token" in str(excinfo.value)


def test_secretservice_init_token_params_invalid() -> None:
    with pytest.raises(ValueError) as excinfo:
        SecretService(token="123456")
    assert "Invalid service token entered" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        SecretService(token="st.1234.4567")
    assert "Invalid service token entered" in str(excinfo.value)


def test_secretservice_init_token_env_invalid() -> None:
    with pytest.raises(ValueError) as excinfo:
        environ["INFISICAL_TOKEN"] = "123456"
        SecretService()
    assert "Invalid service token entered" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        environ["INFISICAL_TOKEN"] = "st.1234.4567"
        SecretService()
    assert "Invalid service token entered" in str(excinfo.value)

    del environ["INFISICAL_TOKEN"]


def test_secretservice_init_token_params_ok() -> None:
    token = "st.64fcd735a54d477d7da0d1bc.4d0d0d27ff4e28a01027efaaf83198aa.0c305d2a033417cdc2d231d34a4b1fd1"
    secret_service = SecretService(token=token)

    assert len(secret_service.service_token_parts) == 4
    assert secret_service.service_token_parts[0] == "st"
    assert secret_service.service_token_parts[1] == "64fcd735a54d477d7da0d1bc"
    assert secret_service.service_token_parts[2] == "4d0d0d27ff4e28a01027efaaf83198aa"
    assert secret_service.service_token_parts[3] == "0c305d2a033417cdc2d231d34a4b1fd1"


def test_secretservice_init_token_env_ok() -> None:
    environ[
        "INFISICAL_TOKEN"
    ] = "st.64fcd735a54d477d7da0d1bc.4d0d0d27ff4e28a01027efaaf83198aa.0c305d2a033417cdc2d231d34a4b1fd1"
    secret_service = SecretService()

    assert len(secret_service.service_token_parts) == 4
    assert secret_service.service_token_parts[0] == "st"
    assert secret_service.service_token_parts[1] == "64fcd735a54d477d7da0d1bc"
    assert secret_service.service_token_parts[2] == "4d0d0d27ff4e28a01027efaaf83198aa"
    assert secret_service.service_token_parts[3] == "0c305d2a033417cdc2d231d34a4b1fd1"

    del environ["INFISICAL_TOKEN"]


def test_secretservice_init_domain_default() -> None:
    token = "st.64fcd735a54d477d7da0d1bc.4d0d0d27ff4e28a01027efaaf83198aa.0c305d2a033417cdc2d231d34a4b1fd1"
    secret_service = SecretService(token=token)

    assert secret_service.infisical_api_url == "https://app.infisical.com/api"


def test_secretservice_init_domain_params() -> None:
    token = "st.64fcd735a54d477d7da0d1bc.4d0d0d27ff4e28a01027efaaf83198aa.0c305d2a033417cdc2d231d34a4b1fd1"
    domain = "https://custom-infisical.example.com/api"
    domain_trailing_slash = "https://custom-infisical.example.com/api/"

    secret_service = SecretService(token=token, domain=domain)

    assert secret_service.infisical_api_url == domain

    secret_service = SecretService(token=token, domain=domain_trailing_slash)

    assert secret_service.infisical_api_url == domain


def test_secretservice_init_domain_env() -> None:
    token = "st.64fcd735a54d477d7da0d1bc.4d0d0d27ff4e28a01027efaaf83198aa.0c305d2a033417cdc2d231d34a4b1fd1"
    domain = "https://custom-infisical.example.com/api"
    domain_trailing_slash = "https://custom-infisical.example.com/api/"

    environ["INFISICAL_API_URL"] = domain
    secret_service = SecretService(token=token)

    assert secret_service.infisical_api_url == domain

    environ["INFISICAL_API_URL"] = domain_trailing_slash
    secret_service = SecretService(token=token)

    assert secret_service.infisical_api_url == domain

    del environ["INFISICAL_API_URL"]


def test_secretservice_get_all_secrets_defaults_params() -> None:
    token = environ["TEST_INFISICAL_TOKEN"]
    domain = environ["TEST_INFISICAL_API_URL"]

    secretService = SecretService(token=token, domain=domain)

    secrets = secretService.get_all()

    assert len(secrets) == 5


def test_secretservice_inject_all_secrets_defaults_params() -> None:
    token = environ["TEST_INFISICAL_TOKEN"]
    domain = environ["TEST_INFISICAL_API_URL"]

    secretService = SecretService(token=token, domain=domain)

    secretService.inject_all()

    assert (
        environ["DATABASE_URL"] == "mongodb+srv://user1234:example_password@mongodb.net"
    )
    assert environ["DB_PASSWORD"] == "example_password"
    assert environ["DB_USERNAME"] == "user1234"
    assert environ["TWILIO_AUTH_TOKEN"] == "example_twillio_token"
    assert environ["WEBSITE_URL"] == "http://localhost:3000"

    del environ["DATABASE_URL"]
    del environ["DB_PASSWORD"]
    del environ["DB_USERNAME"]
    del environ["TWILIO_AUTH_TOKEN"]
    del environ["WEBSITE_URL"]
