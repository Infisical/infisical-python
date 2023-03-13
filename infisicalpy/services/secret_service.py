from typing import List, Tuple, Union

from infisicalpy.api.get_secrets import get_secrets
from infisicalpy.api.get_service_token_data import get_service_token_data
from infisicalpy.api.models import GetServiceTokenDetailsResponse
from infisicalpy.models import InfisicalSecret
from infisicalpy.services.key_service import KeyService
from infisicalpy.utils.crypto import Base64String, Buffer, decrypt_symmetric
from infisicalpy.utils.http import BaseUrlSession


class SecretService:
    @staticmethod
    def get_decrypted_details(
        api_request: BaseUrlSession, key: Union[Buffer, Base64String]
    ) -> Tuple[List[InfisicalSecret], GetServiceTokenDetailsResponse]:
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
        )

        secrets = KeyService.decrypt_secrets(workspace_key, encrypted_secrets.secrets)

        return (secrets, service_token_details)
