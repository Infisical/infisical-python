import os
from typing import Dict, List, Optional

from infisicalpy.api import (
    create_api_request_with_auth,
    get_secrets,
    get_service_token_data,
)
from infisicalpy.api.models import GetEncryptedSecretsV2Request
from infisicalpy.constants import INFISICAL_URL, SECRET_TYPE_PERSONAL
from infisicalpy.models import InfisicalSecret
from infisicalpy.services.key_service import KeyService
from infisicalpy.utils.crypto import decrypt_symmetric


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
        default_values: Optional[Dict[str, str]] = None,
        debug: bool = False,
    ) -> "InfisicalClient":
        instance = InfisicalClient(token=token, site_url=site_url, debug=debug)

        instance.setup(attach_to_process_env, default_values)

        return instance

    def setup(
        self,
        attach_to_process_env: bool = False,
        default_values: Optional[Dict[str, str]] = None,
    ) -> None:
        default_values = default_values if default_values is not None else {}
        self._secrets = default_values

        for default_key, default_value in default_values.items():
            if attach_to_process_env:
                os.environ[default_key] = default_value
            self._infisical_secrets.append(
                InfisicalSecret(
                    key=default_key, value=default_value, type=SECRET_TYPE_PERSONAL
                )
            )

        service_token_details = get_service_token_data(self._api_request)

        encrypted_secrets = get_secrets(
            self._api_request,
            GetEncryptedSecretsV2Request(
                workspaceId=service_token_details.workspace,
                environment=service_token_details.environment,
            ),
        )

        workspace_key = decrypt_symmetric(
            ciphertext=service_token_details.encrypted_key,
            iv=service_token_details.iv,
            tag=service_token_details.tag,
            key=self._key,
        )

        secrets = KeyService.decrypt_secrets(workspace_key, encrypted_secrets)

        self._infisical_secrets = secrets + self._infisical_secrets

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

    def get_secret_value(self, key: str) -> Optional[str]:
        if key in self._secrets:
            return self._secrets[key]

        return os.environ.get(key)
