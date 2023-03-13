import re
from typing import Dict, List, Union

from infisicalpy.api.models import GetEncryptedSecretsV2SecretResponse
from infisicalpy.constants import (
    RESERVED_ENV_VAR_PREFIXES,
    RESERVED_ENV_VARS,
    SECRET_TYPE_PERSONAL,
    SECRET_TYPE_SHARED,
)
from infisicalpy.models import InfisicalSecret
from infisicalpy.utils.crypto import Base64String, Buffer, decrypt_symmetric


class KeyService:
    @staticmethod
    def decrypt_secrets(
        workspace_key: Union[Buffer, Base64String],
        encrypted_secrets: List[GetEncryptedSecretsV2SecretResponse],
    ) -> List[InfisicalSecret]:
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

    @staticmethod
    def override_secrets(
        secrets: List[InfisicalSecret], secret_type: str
    ) -> List[InfisicalSecret]:
        personal_secrets: Dict[str, InfisicalSecret] = {}
        shared_secrets: Dict[str, InfisicalSecret] = {}
        secrets_to_return: List[InfisicalSecret] = []
        secrets_to_return_map: Dict[str, InfisicalSecret] = {}

        for secret in secrets:
            if secret.type == SECRET_TYPE_PERSONAL:
                personal_secrets[secret.key] = secret
            elif secret.type == SECRET_TYPE_SHARED:
                shared_secrets[secret.key] = secret

        if secret_type == SECRET_TYPE_PERSONAL:
            for secret in secrets:
                if secret.key in personal_secrets:
                    secrets_to_return_map[secret.key] = personal_secrets[secret.key]
                else:
                    if secret.key not in secrets_to_return_map:
                        secrets_to_return_map[secret.key] = secret
        elif secret_type == SECRET_TYPE_SHARED:
            for secret in secrets:
                if secret.key in shared_secrets:
                    secrets_to_return_map[secret.key] = shared_secrets[secret.key]
                else:
                    if secret.key not in secrets_to_return_map:
                        secrets_to_return_map[secret.key] = secret

        for secret in secrets_to_return_map.values():
            secrets_to_return.append(secret)

        return secrets_to_return

    @staticmethod
    def substitute_secrets(
        secrets: List[InfisicalSecret],
    ) -> List[InfisicalSecret]:
        hashmap_of_complete_variables: Dict[str, str] = {}
        hashmap_of_self_refs: Dict[str, str] = {}
        expanded_secrets: List[InfisicalSecret] = []

        for secret in secrets:
            expanded_variable = KeyService._get_expanded_env_variable(
                secrets, secret.key, hashmap_of_complete_variables, hashmap_of_self_refs
            )

            secret_copy = secret.copy(deep=True)
            secret_copy.value = expanded_variable
            expanded_secrets.append(secret_copy)

        return expanded_secrets

    @staticmethod
    def _get_expanded_env_variable(
        secrets: List[InfisicalSecret],
        variable_we_are_looking_for: str,
        hashmap_of_complete_variables: Dict[str, str],
        hashmap_of_self_refs: Dict[str, str],
    ) -> str:
        if variable_we_are_looking_for in hashmap_of_complete_variables:
            return hashmap_of_complete_variables[variable_we_are_looking_for]

        regex = re.compile(r"\${[^\}]*}")

        for secret in secrets:
            if secret.key != variable_we_are_looking_for:
                continue

            variables_to_populate: List[str] = regex.findall(secret.value)

            if len(variables_to_populate) == 0:
                return secret.value

            value_to_edit = secret.value
            for variable_with_sign in variables_to_populate:
                variable_without_sign = variable_with_sign.lstrip("${").rstrip("}")

                # case: reference to self
                if variable_without_sign == secret.key:
                    hashmap_of_self_refs[variable_without_sign] = variable_without_sign
                    continue

                if variable_without_sign in hashmap_of_complete_variables:
                    expanded_variable_value = hashmap_of_complete_variables[
                        variable_without_sign
                    ]
                else:
                    expanded_variable_value = KeyService._get_expanded_env_variable(
                        secrets,
                        variable_without_sign,
                        hashmap_of_complete_variables,
                        hashmap_of_self_refs,
                    )
                    hashmap_of_complete_variables[
                        variable_without_sign
                    ] = expanded_variable_value

                if variable_without_sign in hashmap_of_self_refs:
                    continue
                else:
                    value_to_edit = value_to_edit.replace(
                        variable_with_sign, expanded_variable_value
                    )

            return value_to_edit

        return "${" + variable_we_are_looking_for + "}"

    @staticmethod
    def filter_reserved_env_vars(env: Dict[str, InfisicalSecret]) -> None:
        for reserved_env_name in RESERVED_ENV_VARS:
            if reserved_env_name in env:
                del env[reserved_env_name]
                print("Reserved name!")
        for reserved_env_prefix in RESERVED_ENV_VAR_PREFIXES:
            for env_name in env.keys():
                if env_name.startswith(reserved_env_prefix):
                    del env[env_name]
                    print("Reserved prefix!")
