import os
from typing import Dict, Optional

from infisical.api import create_api_request_with_auth
from infisical.constants import INFISICAL_URL, SERVICE_TOKEN_REGEX
from infisical.exceptions import InfisicalTokenError
from infisical.logger import logger
from infisical.services.secret_service import SecretService


class InfisicalClient:
    def __init__(
        self, token: str, site_url: str = INFISICAL_URL, debug: bool = False
    ) -> None:
        """Verify the token and initialize the client.

        :param token: The Infisical Token to use to connect to Infisical
        :param site_url: The URL of Infisical to connect to, defaults to the cloud API
        :param debug: Display error messages, defaults to False
        :raises InfisicalTokenError: If token is empty or malformated
        """
        if len(token) == 0:
            raise InfisicalTokenError("The token must not be empty!")

        token_match = SERVICE_TOKEN_REGEX.fullmatch(token)

        if token_match is None:
            raise InfisicalTokenError("The token is not in correct format!")

        service_token = token_match.group(1)
        key = token_match.group(2)

        self._api_request = create_api_request_with_auth(site_url, service_token)
        self._key = key.encode("utf-8")

        self._debug = debug
        self._secrets: Dict[str, str] = {}

    @staticmethod
    def connect(
        token: str,
        site_url: str = INFISICAL_URL,
        attach_to_process_env: bool = False,
        debug: bool = False,
    ) -> "InfisicalClient":
        """Connect to Infisical and return a new instance of :class:`InfisicalClient`

        :param token: The Infisical Token to use to connect to Infisical
        :param site_url: The URL of Infisical to connect to, defaults to the cloud API
        :param attach_to_process_env: Inject the secrets in `os.environ`, defaults to False
        :param debug: Display error messages, defaults to False
        :return: A new instance of :class:`InfisicalClient`
        """
        instance = InfisicalClient(token=token, site_url=site_url, debug=debug)

        instance.setup(attach_to_process_env)

        return instance

    def setup(
        self,
        attach_to_process_env: bool = False,
    ) -> None:
        """Sets up the Infisical client by getting data and secrets associated
        with the instance's Infisical token

        :param attach_to_process_env: Inject the secrets in `os.environ`, defaults to False
        """
        try:
            secrets, _ = SecretService.get_decrypted_details(
                api_request=self._api_request, key=self._key
            )

            for secret in secrets:
                self._secrets[secret.key] = secret.value
                if attach_to_process_env:
                    os.environ[secret.key] = secret.value
        except Exception as exc:
            if self._debug:
                logger.exception(exc)
                logger.error(
                    "Failed to set up the Infisical client. Please ensure that your token is valid and try again."
                )

    def get(self, key: str) -> Optional[str]:
        """Return value for secret with key `key`.

        :param key: Key of secret
        :return: Value of secret or None if not found
        """
        value: Optional[str] = None

        if key in self._secrets:
            value = self._secrets[key]
        else:
            value = os.environ.get(key)

        if value is None and self._debug:
            logger.warning(
                f"Warning: Missing value for '{key}'. Please check your configuration."
            )

        return value
