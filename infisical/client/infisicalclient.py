import json
from typing import Dict, Optional

from infisical.api import create_api_request_with_auth
from infisical.constants import (
    AUTH_MODE_SERVICE_TOKEN,
    AUTH_MODE_SERVICE_TOKEN_V3,
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
from infisical.utils.crypto import (
    create_symmetric_key_helper,
    decrypt_symmetric_helper,
    encrypt_symmetric_helper,
)
from typing_extensions import Literal


class InfisicalClient:
    def __init__(
        self,
        token: Optional[str] = None,
        token_json: Optional[str] = None,
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
        
        if token_json and token_json != "":
            token_dict = json.loads(token_json)
            
            self.client_config = ClientConfig(
                auth_mode=AUTH_MODE_SERVICE_TOKEN_V3,
                credentials={
                    "public_key": token_dict["publicKey"],
                    "private_key": token_dict["privateKey"]
                },
                cache_ttl=cache_ttl
            )

            self.api_request = create_api_request_with_auth(site_url, token_dict["serviceToken"])

        self.debug = debug

    def get_all_secrets(
        self, 
        environment: str = "dev", 
        path: str = "/", 
        include_imports: bool = True,
        attach_to_os_environ: bool = False
    ):
        """Return all the secrets accessible by the instance of Infisical"""
        return get_all_secrets_helper(self, environment, path, include_imports, attach_to_os_environ)

    def get_secret(
        self,
        secret_name: str,
        type: Literal["shared", "personal"] = "personal",
        environment: str = "dev",
        path: str = "/",
    ) -> SecretBundle:
        """Return secret with name `secret_name`

        :param secret_name: Key of secret
        :param type: Type of secret that is either "shared" or "personal"
        :return: Secret bundle for secret with name `secret_name`
        """
        return get_secret_helper(self, secret_name, type, environment, path)

    def create_secret(
        self,
        secret_name: str,
        secret_value: str,
        type: Literal["shared", "personal"] = "shared",
        environment: str = "dev",
        path: str = "/",
    ) -> SecretBundle:
        """Create secret with name `secret_name` and value `secret_value`

        :param secret_name: Name of secret to create
        :param secret_value: Value of secret to create
        :param type: Type of secret to create that is either "shared" or "personal"
        :return: Secret bundle for created secret with name `secret_name`
        """
        return create_secret_helper(
            self, secret_name, secret_value, type, environment, path
        )

    def update_secret(
        self,
        secret_name: str,
        secret_value: str,
        type: Literal["shared", "personal"] = "shared",
        environment: str = "dev",
        path: str = "/",
    ) -> SecretBundle:
        """Update secret with name `secret_name` and value `secret_value`

        :param secret_name: Name of secret to update
        :param secret_value: New value of secret to update
        :param type: Type of secret to update that is either "shared" or "personal"
        :return: Secret bundle for updated secret with name `secret_name`
        """
        return update_secret_helper(
            self, secret_name, secret_value, type, environment, path
        )

    def delete_secret(
        self,
        secret_name: str,
        type: Literal["shared", "personal"] = "shared",
        environment: str = "dev",
        path: str = "/",
    ):
        """Delete secret with name `secret_name`

        :param secret_name: Name of secret to delete
        :param type: Type of secret to update that is either "shared" or "personal"
        :return: Secret bundle for updated secret with name `secret_name`
        """
        return delete_secret_helper(self, secret_name, type, environment, path)

    def create_symmetric_key(self) -> str:
        """Create a base64-encoded, 256-bit symmetric key"""
        return create_symmetric_key_helper()

    def encrypt_symmetric(self, plaintext: str, key: str):
        """Encrypt the plaintext `plaintext` with the (base64) 256-bit secret key `key`"""
        return encrypt_symmetric_helper(plaintext, key)

    def decrypt_symmetric(self, ciphertext: str, key: str, iv: str, tag: str):
        """Decrypt the ciphertext `ciphertext` with the (base64) 256-bit secret key `key`, provided `iv` and `tag`"""
        return decrypt_symmetric_helper(ciphertext, key, iv, tag)
