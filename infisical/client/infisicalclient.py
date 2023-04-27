from typing import Dict, Optional

from infisical.api import create_api_request_with_auth
from infisical.constants import (
    AUTH_MODE_SERVICE_TOKEN,
    INFISICAL_URL,
    SERVICE_TOKEN_REGEX,
)
from infisical.exceptions import InfisicalTokenError
from infisical.helpers.client import (
    create_secret_helper,
    delete_secret_helper,
    get_all_secrets_helper,
    get_secret_helper,
    update_secret_helper,
)
from infisical.models.models import SecretBundle
from infisical.models.secret_service import ClientConfig
from typing_extensions import Literal


class InfisicalClient:
    def __init__(
        self,
        token: Optional[str] = None,
        site_url: str = INFISICAL_URL,
        debug: bool = False,
        cache_ttl: int = 300,
    ):
        self.cache: Dict[str, SecretBundle] = {}
        self.client_config: Optional[ClientConfig] = None

        if token and token != "":
            token_match = SERVICE_TOKEN_REGEX.fullmatch(token)

            if token_match is None:
                raise InfisicalTokenError("The token is not in correct format!")

            service_token = token_match.group(1)
            service_token_key = token_match.group(2)

            self.client_config = ClientConfig(
                auth_mode=AUTH_MODE_SERVICE_TOKEN,
                credentials={"service_token_key": service_token_key},
                cache_ttl=cache_ttl,
            )

            self.api_request = create_api_request_with_auth(site_url, service_token)

        self.debug = debug

    def get_all_secrets(self):
        """Return all the secrets accessible by the instance of Infisical"""
        return get_all_secrets_helper(self)

    def get_secret(
        self, secret_name: str, type: Literal["shared", "personal"] = "personal"
    ) -> SecretBundle:
        """Return secret with name `secret_name`

        :param secret_name: Key of secret
        :param type: Type of secret that is either "shared" or "personal"
        :return: Secret bundle for secret with name `secret_name`
        """
        return get_secret_helper(self, secret_name, type)

    def create_secret(
        self,
        secret_name: str,
        secret_value: str,
        type: Literal["shared", "personal"] = "shared",
    ):
        """Create secret with name `secret_name` and value `secret_value`

        :param secret_name: Name of secret to create
        :param secret_value: Value of secret to create
        :param type: Type of secret to create that is either "shared" or "personal"
        :return: Secret bundle for created secret with name `secret_name`
        """
        return create_secret_helper(self, secret_name, secret_value, type)

    def update_secret(
        self,
        secret_name: str,
        secret_value: str,
        type: Literal["shared", "personal"] = "shared",
    ):
        """Update secret with name `secret_name` and value `secret_value`

        :param secret_name: Name of secret to update
        :param secret_value: New value of secret to update
        :param type: Type of secret to update that is either "shared" or "personal"
        :return: Secret bundle for updated secret with name `secret_name`
        """
        return update_secret_helper(self, secret_name, secret_value, type)

    def delete_secret(
        self, secret_name: str, type: Literal["shared", "personal"] = "shared"
    ):
        """Delete secret with name `secret_name`

        :param secret_name: Name of secret to delete
        :param type: Type of secret to update that is either "shared" or "personal"
        :return: Secret bundle for updated secret with name `secret_name`
        """
        return delete_secret_helper(self, secret_name, type)
