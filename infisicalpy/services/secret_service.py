from typing import List, Tuple, Union

from infisicalpy.api.get_secrets import get_secrets
from infisicalpy.api.get_service_token_data import get_service_token_data
from infisicalpy.api.models import GetServiceTokenDetailsResponse
from infisicalpy.models import InfisicalSecret
from infisicalpy.services.key_service import KeyService
from infisicalpy.utils.crypto import Base64String, Buffer, decrypt_symmetric
from requests import Session


class SecretService:
    @staticmethod
    def get_decrypted_details(
        api_request: Session, key: Union[Buffer, Base64String]
    ) -> Tuple[List[InfisicalSecret], GetServiceTokenDetailsResponse]:
        """Returns a tuple containing the secrets decrypted and the service token data.
        This method use the ``api_request`` client to perform the requests. It should be configured
        on a service token.

        :param api_request: The :class:`requests.Session` instance authenticated
        :param key: The symmetric decryption key from the service token
        :return: Returns a tuple containing the secrets decrypted and the service token data
        """
        service_token_details = get_service_token_data(api_request)

        encrypted_secrets = get_secrets(
            api_request,
            workspace_id=service_token_details.workspace,
            environment=service_token_details.environment,
        )

        workspace_key = decrypt_symmetric(
            ciphertext=service_token_details.encrypted_key,
            iv=service_token_details.iv,
            tag=service_token_details.tag,
            key=key,
        ).encode("utf-8")

        secrets = KeyService.decrypt_secrets(workspace_key, encrypted_secrets.secrets)

        return (secrets, service_token_details)
