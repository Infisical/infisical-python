from os import environ
from typing import List, Optional

from infisicalpy.api import api
from infisicalpy.api.models import GetEncryptedSecretsV2Request
from infisicalpy.constants import (
    INFISICAL_API_URL_NAME,
    INFISICAL_DEFAULT_API_URL,
    INFISICAL_TOKEN_NAME,
    SECRET_TYPE_PERSONAL,
    SECRET_TYPE_SHARED,
)
from infisicalpy.core.http import get_client
from infisicalpy.crypto import decrypt_symmetric
from infisicalpy.models import SingleEnvironmentVariable
from infisicalpy.utils.helpers import get_base64_decoded_symmetric_encryption_details
from infisicalpy.utils.secrets import (
    filter_reserved_env_vars,
    get_plaintext_secrets,
    override_secrets,
    substitute_secrets,
)


class SecretService:
    def __init__(
        self, token: Optional[str] = None, domain: Optional[str] = None
    ) -> None:
        if token is None:
            token = environ.get(INFISICAL_TOKEN_NAME)

            if token is None:
                raise ValueError(
                    "Cannot find infisical token! Please provide it as a parameter or via the INFISICAL_TOKEN environment variable"
                )

        self.service_token_parts = token.split(".", 4)
        if len(self.service_token_parts) < 4:
            raise ValueError(
                "Invalid service token entered. Please double check your service token and try again"
            )

        if domain is not None:
            self.infisical_api_url = domain.rstrip("/")
        else:
            domain = environ.get(INFISICAL_API_URL_NAME)

            self.infisical_api_url = (
                domain.rstrip("/") if domain is not None else INFISICAL_DEFAULT_API_URL
            )

    def get_all(
        self,
        expand: bool = True,
        secret_overriding: bool = True,
        tags: Optional[List[str]] = None,
    ) -> List[SingleEnvironmentVariable]:
        service_token = ".".join(
            [
                self.service_token_parts[0],
                self.service_token_parts[1],
                self.service_token_parts[2],
            ]
        )

        http_client = get_client()

        http_client.headers.update({"Authorization": f"Bearer {service_token}"})

        service_token_details = api.call_get_service_token_details_v2(
            http_client, self.infisical_api_url
        )

        encrypted_secrets = api.call_get_secrets_v2(
            http_client,
            self.infisical_api_url,
            GetEncryptedSecretsV2Request(
                workspaceId=service_token_details.workspace,
                environment=service_token_details.environment,
                tagSlugs=",".join(tags) if tags is not None else "",
            ),
        )

        decoded_symmetric_encryption_details = (
            get_base64_decoded_symmetric_encryption_details(
                self.service_token_parts[3],
                service_token_details.encrypted_key,
                service_token_details.iv,
                service_token_details.tag,
            )
        )

        plaintext_workspace_key = decrypt_symmetric(
            bytes(self.service_token_parts[3], "utf-8"),
            decoded_symmetric_encryption_details.cipher,
            decoded_symmetric_encryption_details.tag,
            decoded_symmetric_encryption_details.iv,
        )

        secrets = get_plaintext_secrets(plaintext_workspace_key, encrypted_secrets)

        if secret_overriding:
            secrets = override_secrets(secrets, SECRET_TYPE_PERSONAL)
        else:
            secrets = override_secrets(secrets, SECRET_TYPE_SHARED)

        if expand:
            secrets = substitute_secrets(secrets)

        secrets_by_key = {secret.key: secret for secret in secrets}

        filter_reserved_env_vars(secrets_by_key)

        return list(secrets_by_key.values())

    def inject_all(
        self,
        expand: bool = True,
        secret_overriding: bool = True,
        tags: Optional[List[str]] = None,
    ) -> None:
        secrets = self.get_all(
            expand=expand, secret_overriding=secret_overriding, tags=tags
        )

        for secret in secrets:
            environ[secret.key] = secret.value
