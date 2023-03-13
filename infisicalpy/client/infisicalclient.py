import os
from typing import Dict, List, Optional

from infisicalpy.api import create_api_request_with_auth
from infisicalpy.constants import INFISICAL_URL
from infisicalpy.logger import logger
from infisicalpy.models import InfisicalSecret
from infisicalpy.services.secret_service import SecretService


class InfisicalClient:
    def __init__(self, token: str, site_url: str, debug: bool) -> None:
        last_dot_idx = token.rindex(".")
        service_token = token[0:last_dot_idx]
        key = token[last_dot_idx + 1 :]

        self._api_request = create_api_request_with_auth(site_url, service_token)
        self._key = key
        self._workspace_id = ""
        self._environment = ""
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
        instance = InfisicalClient(token=token, site_url=site_url, debug=debug)

        instance.setup(attach_to_process_env)

        return instance

    def setup(
        self,
        attach_to_process_env: bool = False,
    ) -> None:
        secrets, service_token_data = SecretService.get_decrypted_details(
            api_request=self._api_request, key=self._key
        )

        self._workspace_id = service_token_data.workspace
        self._environment = service_token_data.environment

        self._infisical_secrets = secrets

        # if secret_overriding:
        #     self._infisical_secrets = KeyService.override_secrets(secrets, SECRET_TYPE_PERSONAL)
        # else:
        #     self._infisical_secrets = KeyService.override_secrets(secrets, SECRET_TYPE_SHARED)

        # if expand:
        #     self._infisical_secrets = KeyService.substitute_secrets(secrets)

        # secrets_by_key = {secret.key: secret for secret in self._infisical_secrets}

        # KeyService.filter_reserved_env_vars(secrets_by_key)

        for secret in secrets:
            self._secrets[secret.key] = secret.value
            if attach_to_process_env:
                os.environ[secret.key] = secret.value

    def get(self, key: str) -> Optional[str]:
        value: Optional[str] = None

        if key in self._secrets:
            value = self._secrets[key]
        value = os.environ.get(key)

        if value is None and self._debug:
            logger.warning(
                f"Warning: Missing value for '{key}'. Please check your configuration."
            )

        return value
