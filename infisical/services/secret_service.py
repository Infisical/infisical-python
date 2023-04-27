from datetime import datetime
from typing import List

from infisical.api.create_secret import create_secret_req
from infisical.api.delete_secret import delete_secret_req
from infisical.api.get_secret import get_secret_req
from infisical.api.get_secrets import get_secrets_req
from infisical.api.get_service_token_data import get_service_token_data_req
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
from infisical.models.secret_service import ClientConfig, WorkspaceConfig
from infisical.utils.crypto import decrypt_symmetric, encrypt_symmetric
from requests import Session
from typing_extensions import Literal


class SecretService:
    @staticmethod
    def populate_client_config(
        api_request: Session, client_config: ClientConfig
    ) -> WorkspaceConfig:
        service_token_details = get_service_token_data_req(api_request)

        workspace_key = decrypt_symmetric(
            ciphertext=service_token_details.encrypted_key,
            iv=service_token_details.iv,
            tag=service_token_details.tag,
            key=client_config.credentials["service_token_key"],
        )

        return WorkspaceConfig(
            workspace_id=service_token_details.workspace,
            environment=service_token_details.environment,
            workspace_key=workspace_key,
        )

    @staticmethod
    def get_fallback_secret(secret_name: str) -> SecretBundle:
        return SecretBundle(
            secret_name=secret_name,
            secret_value=None,
            is_fallback=True,
            last_fetched_at=datetime.now(),
        )

    @staticmethod
    def get_decrypted_secrets(
        api_request: Session, workspace_key: str, workspace_id: str, environment: str
    ) -> List[SecretBundle]:
        options = GetSecretsDTO(workspace_id=workspace_id, environment=environment)

        encrypted_secrets = get_secrets_req(api_request, options)

        secret_bundles: List[SecretBundle] = []

        for encrypted_secret in encrypted_secrets.secrets:
            secret_name = decrypt_symmetric(
                ciphertext=encrypted_secret.secret_key_ciphertext,
                iv=encrypted_secret.secret_key_iv,
                tag=encrypted_secret.secret_key_tag,
                key=workspace_key,
            )

            secret_value = decrypt_symmetric(
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
    ):
        options = GetSecretDTO(
            secret_name=secret_name,
            workspace_id=workspace_id,
            environment=environment,
            type=type,
        )

        encrypted_secret = get_secret_req(
            api_request,
            options,
        )

        secret_value = decrypt_symmetric(
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
    ):
        secret_key_ciphertext, secret_key_iv, secret_key_tag = encrypt_symmetric(
            plaintext=secret_name, key=workspace_key
        )

        secret_value_ciphertext, secret_value_iv, secret_value_tag = encrypt_symmetric(
            plaintext=secret_value, key=workspace_key
        )

        options = CreateSecretDTO(
            secret_name=secret_name,
            workspace_id=workspace_id,
            environment=environment,
            type=type,
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
    ):
        secret_value_ciphertext, secret_value_iv, secret_value_tag = encrypt_symmetric(
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
        secret_name: str,
    ):
        options = DeleteSecretDTO(
            secret_name=secret_name,
            workspace_id=workspace_id,
            environment=environment,
            type=type,
        )

        encrypted_secret = delete_secret_req(api_request, options)

        secret_value = decrypt_symmetric(
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
