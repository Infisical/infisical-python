from typing import List, Union

from infisical.api.models import GetEncryptedSecretsV2SecretResponse
from infisical.models import InfisicalSecret
from infisical.utils.crypto import Base64String, Buffer, decrypt_symmetric


class KeyService:
    @staticmethod
    def decrypt_secrets(
        workspace_key: Union[Buffer, Base64String],
        encrypted_secrets: List[GetEncryptedSecretsV2SecretResponse],
    ) -> List[InfisicalSecret]:
        """Returns the decrypted secrets.

        :param workspace_key: The key of the workspace for symmetrical decryption
        :param encrypted_secrets: The secrets encrypted along with decryption parameters
        :return: The plain version of the secrets
        """
        secrets: List[InfisicalSecret] = []

        for secret in encrypted_secrets:
            key = decrypt_symmetric(
                ciphertext=secret.secret_key_ciphertext,
                iv=secret.secret_key_iv,
                tag=secret.secret_key_tag,
                key=workspace_key,
            )

            value = decrypt_symmetric(
                ciphertext=secret.secret_value_ciphertext,
                iv=secret.secret_value_iv,
                tag=secret.secret_value_tag,
                key=workspace_key,
            )

            secrets.append(InfisicalSecret(key=key, value=value, type=secret.type))

        return secrets
