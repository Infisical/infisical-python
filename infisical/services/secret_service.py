import os
from typing import List

from infisical.api.create_secret import create_secret_req
from infisical.api.delete_secret import delete_secret_req
from infisical.api.get_secret import get_secret_req
from infisical.api.get_secrets import get_secrets_req
from infisical.api.get_service_token_data import get_service_token_data_req
from infisical.api.get_service_token_data_key import get_service_token_data_key_req
from infisical.api.update_secret import update_secret_req
from infisical.helpers.secrets import transform_secret_to_secret_bundle
from infisical.models.api import (
    CreateSecretDTO,
    DeleteSecretDTO,
    GetSecretDTO,
    GetSecretsDTO,
    UpdateSecretDTO,
)
from infisical.models.models import SecretBundle
from infisical.models.secret_service import (
    ClientConfig,
    ServiceTokenCredentials,
    ServiceTokenV3Credentials,
    WorkspaceConfig,
)
from infisical.utils.crypto import (
    decrypt_asymmetric,
    decrypt_symmetric_128_bit_hex_key_utf8,
    encrypt_symmetric_128_bit_hex_key_utf8,
)
from requests import Session
from typing_extensions import Literal


class SecretService:
    @staticmethod
    def populate_client_config(
        api_request: Session, client_config: ClientConfig
    ) -> WorkspaceConfig:
        if client_config.auth_mode == "service_token" and isinstance(
            client_config.credentials, ServiceTokenCredentials
        ):
            service_token_details = get_service_token_data_req(api_request)
            workspace_key = decrypt_symmetric_128_bit_hex_key_utf8(
                ciphertext=service_token_details.encrypted_key,
                iv=service_token_details.iv,
                tag=service_token_details.tag,
                key=client_config.credentials.service_token_key,
            )

            return WorkspaceConfig(
                workspace_id=service_token_details.workspace,
                workspace_key=workspace_key,
            )

        if client_config.auth_mode == "service_token_v3" and isinstance(
            client_config.credentials, ServiceTokenV3Credentials
        ):
            service_token_key_details = get_service_token_data_key_req(api_request)
            workspace_key = decrypt_asymmetric(
                ciphertext=service_token_key_details.key.encrypted_key,
                nonce=service_token_key_details.key.nonce,
                public_key=service_token_key_details.key.public_key,
                private_key=client_config.credentials.private_key,
            )

            return WorkspaceConfig(
                workspace_id=service_token_key_details.key.workspace,
                workspace_key=workspace_key,
            )
        raise Exception("Failed to identify the auth mode!")

    @staticmethod
    def get_fallback_secret(secret_name: str) -> SecretBundle:
        return SecretBundle(
            secret_name=secret_name,
            secret_value=os.environ[secret_name],
            is_fallback=True,
        )

    @staticmethod
    def get_decrypted_secrets(
        api_request: Session,
        workspace_key: str,
        workspace_id: str,
        environment: str,
        path: str,
        include_imports: bool,
    ) -> List[SecretBundle]:
        options = GetSecretsDTO(
            workspace_id=workspace_id,
            environment=environment,
            path=path,
            include_imports=include_imports,
        )

        encrypted_secrets, secret_imports = get_secrets_req(api_request, options)

        secret_bundles: List[SecretBundle] = []

        for encrypted_secret in encrypted_secrets:
            secret_name = decrypt_symmetric_128_bit_hex_key_utf8(
                ciphertext=encrypted_secret.secret_key_ciphertext,
                iv=encrypted_secret.secret_key_iv,
                tag=encrypted_secret.secret_key_tag,
                key=workspace_key,
            )

            secret_value = decrypt_symmetric_128_bit_hex_key_utf8(
                ciphertext=encrypted_secret.secret_value_ciphertext,
                iv=encrypted_secret.secret_value_iv,
                tag=encrypted_secret.secret_value_tag,
                key=workspace_key,
            )

            secret_bundles.append(
                transform_secret_to_secret_bundle(
                    secret=encrypted_secret,
                    secret_name=secret_name,
                    secret_value=secret_value,
                )
            )

        for secret_import in secret_imports:
            for encrypted_secret in secret_import.secrets:
                secret_name = decrypt_symmetric_128_bit_hex_key_utf8(
                    ciphertext=encrypted_secret.secret_key_ciphertext,
                    iv=encrypted_secret.secret_key_iv,
                    tag=encrypted_secret.secret_key_tag,
                    key=workspace_key,
                )

                secret_value = decrypt_symmetric_128_bit_hex_key_utf8(
                    ciphertext=encrypted_secret.secret_value_ciphertext,
                    iv=encrypted_secret.secret_value_iv,
                    tag=encrypted_secret.secret_value_tag,
                    key=workspace_key,
                )

                secret_bundles.append(
                    transform_secret_to_secret_bundle(
                        secret=encrypted_secret,
                        secret_name=secret_name,
                        secret_value=secret_value,
                    )
                )

        return secret_bundles

    @staticmethod
    def get_decrypted_secret(
        api_request: Session,
        secret_name: str,
        workspace_id: str,
        environment: str,
        workspace_key: str,
        type: Literal["shared", "personal"],
        path: str,
    ) -> SecretBundle:
        options = GetSecretDTO(
            secret_name=secret_name,
            workspace_id=workspace_id,
            environment=environment,
            type=type,
            path=path,
        )

        encrypted_secret = get_secret_req(
            api_request,
            options,
        )

        secret_value = decrypt_symmetric_128_bit_hex_key_utf8(
            ciphertext=encrypted_secret.secret.secret_value_ciphertext,
            iv=encrypted_secret.secret.secret_value_iv,
            tag=encrypted_secret.secret.secret_value_tag,
            key=workspace_key,
        )

        return transform_secret_to_secret_bundle(
            secret=encrypted_secret.secret,
            secret_name=secret_name,
            secret_value=secret_value,
        )

    @staticmethod
    def create_secret(
        api_request: Session,
        workspace_key: str,
        workspace_id: str,
        environment: str,
        type: Literal["shared", "personal"],
        secret_name: str,
        secret_value: str,
        path: str,
    ) -> SecretBundle:
        (
            secret_key_ciphertext,
            secret_key_iv,
            secret_key_tag,
        ) = encrypt_symmetric_128_bit_hex_key_utf8(
            plaintext=secret_name, key=workspace_key
        )

        (
            secret_value_ciphertext,
            secret_value_iv,
            secret_value_tag,
        ) = encrypt_symmetric_128_bit_hex_key_utf8(
            plaintext=secret_value, key=workspace_key
        )

        options = CreateSecretDTO(
            secret_name=secret_name,
            workspace_id=workspace_id,
            environment=environment,
            type=type,
            path=path,
            secret_key_ciphertext=secret_key_ciphertext,
            secret_key_iv=secret_key_iv,
            secret_key_tag=secret_key_tag,
            secret_value_ciphertext=secret_value_ciphertext,
            secret_value_iv=secret_value_iv,
            secret_value_tag=secret_value_tag,
        )

        encrypted_secret = create_secret_req(api_request, options)

        return transform_secret_to_secret_bundle(
            secret=encrypted_secret.secret,
            secret_name=secret_name,
            secret_value=secret_value,
        )

    @staticmethod
    def update_secret(
        api_request: Session,
        workspace_key: str,
        workspace_id: str,
        environment: str,
        type: Literal["shared", "personal"],
        secret_name: str,
        secret_value: str,
        path: str,
    ) -> SecretBundle:
        (
            secret_value_ciphertext,
            secret_value_iv,
            secret_value_tag,
        ) = encrypt_symmetric_128_bit_hex_key_utf8(
            plaintext=secret_value, key=workspace_key
        )

        options = UpdateSecretDTO(
            secret_name=secret_name,
            workspace_id=workspace_id,
            environment=environment,
            type=type,
            secret_value_ciphertext=secret_value_ciphertext,
            secret_value_iv=secret_value_iv,
            secret_value_tag=secret_value_tag,
            path=path,
        )

        encrypted_secret = update_secret_req(api_request, options)
        return transform_secret_to_secret_bundle(
            secret=encrypted_secret.secret,
            secret_name=secret_name,
            secret_value=secret_value,
        )

    @staticmethod
    def delete_secret(
        api_request: Session,
        workspace_key: str,
        workspace_id: str,
        environment: str,
        type: Literal["shared", "personal"],
        path: str,
        secret_name: str,
    ) -> SecretBundle:
        options = DeleteSecretDTO(
            secret_name=secret_name,
            workspace_id=workspace_id,
            environment=environment,
            type=type,
            path=path,
        )

        encrypted_secret = delete_secret_req(api_request, options)

        secret_value = decrypt_symmetric_128_bit_hex_key_utf8(
            ciphertext=encrypted_secret.secret.secret_value_ciphertext,
            iv=encrypted_secret.secret.secret_value_iv,
            tag=encrypted_secret.secret.secret_value_tag,
            key=workspace_key,
        )

        return transform_secret_to_secret_bundle(
            secret=encrypted_secret.secret,
            secret_name=secret_name,
            secret_value=secret_value,
        )
