import os
from typing import Dict, List, Optional

from infisicalpy.api import create_api_request_with_auth
from infisicalpy.constants import INFISICAL_URL
from infisicalpy.logger import logger
from infisicalpy.models import InfisicalSecret
from infisicalpy.services.secret_service import SecretService


class InfisicalClient:
    def __init__(
        self, token: str, site_url: str = INFISICAL_URL, debug: bool = False
    ) -> None:
        last_dot_idx = token.rindex(".")
        service_token = token[0:last_dot_idx]
        key = token[last_dot_idx + 1 :]

        self._api_request = create_api_request_with_auth(site_url, service_token)
        self._key = key.encode("utf-8")

        self._debug = debug
        self._secrets: Dict[str, str] = {}
        self._infisical_secrets: List[InfisicalSecret] = []

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
        secrets, _ = SecretService.get_decrypted_details(
            api_request=self._api_request, key=self._key
        )

        self._infisical_secrets = secrets

        # TODO: Implements secret override and value expanding?
        # if secret_overriding:
        #     self._infisical_secrets = KeyService.override_secrets(secrets, SECRET_TYPE_PERSONAL)
        # else:
        #     self._infisical_secrets = KeyService.override_secrets(secrets, SECRET_TYPE_SHARED)

        # if expand:
        #     self._infisical_secrets = KeyService.substitute_secrets(secrets)

        for secret in secrets:
            self._secrets[secret.key] = secret.value
            if attach_to_process_env:
                os.environ[secret.key] = secret.value

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
