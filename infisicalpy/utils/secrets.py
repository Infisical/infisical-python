import base64
import re
from typing import Dict, List

from infisicalpy.api.models import GetEncryptedSecretsV2Response
from infisicalpy.constants import (
    PERSONAL_SECRET_TYPE_NAME,
    RESERVED_ENV_VAR_PREFIXES,
    RESERVED_ENV_VARS,
    SHARED_SECRET_TYPE_NAME,
)
from infisicalpy.crypto import decrypt_symmetric
from infisicalpy.models import SingleEnvironmentVariable, Tag


def get_plaintext_secrets(
    key: bytes, encrypted_secrets: GetEncryptedSecretsV2Response
) -> List[SingleEnvironmentVariable]:
    plaintext_secrets: List[SingleEnvironmentVariable] = []

    for secret in encrypted_secrets.secrets:
        key_iv = base64.standard_b64decode(secret.secret_key_iv)
        key_tag = base64.standard_b64decode(secret.secret_key_tag)
        key_ciphertext = base64.standard_b64decode(secret.secret_key_ciphertext)

        plaintext_key = decrypt_symmetric(key, key_ciphertext, key_tag, key_iv)

        value_iv = base64.standard_b64decode(secret.secret_value_iv)
        value_tag = base64.standard_b64decode(secret.secret_value_tag)
        value_ciphertext = base64.standard_b64decode(secret.secret_value_ciphertext)

        plaintext_value = decrypt_symmetric(key, value_ciphertext, value_tag, value_iv)

        comment_iv = base64.standard_b64decode(secret.secret_comment_iv)
        comment_tag = base64.standard_b64decode(secret.secret_comment_tag)
        comment_ciphertext = base64.standard_b64decode(secret.secret_comment_ciphertext)

        plaintext_comment = decrypt_symmetric(
            key, comment_ciphertext, comment_tag, comment_iv
        )

        plaintext_secrets.append(
            SingleEnvironmentVariable(
                key=plaintext_key.decode("utf-8"),
                value=plaintext_value.decode("utf-8"),
                type=secret.type,
                _id=secret.id,
                tags=[Tag.parse_obj(tag.dict(by_alias=True)) for tag in secret.tags],
                comment=plaintext_comment.decode("utf-8"),
            )
        )

    return plaintext_secrets


def override_secrets(
    secrets: List[SingleEnvironmentVariable], secret_type: str
) -> List[SingleEnvironmentVariable]:
    personal_secrets: Dict[str, SingleEnvironmentVariable] = {}
    shared_secrets: Dict[str, SingleEnvironmentVariable] = {}
    secrets_to_return: List[SingleEnvironmentVariable] = []
    secrets_to_return_map: Dict[str, SingleEnvironmentVariable] = {}

    for secret in secrets:
        if secret.type == PERSONAL_SECRET_TYPE_NAME:
            personal_secrets[secret.key] = secret
        elif secret.type == SHARED_SECRET_TYPE_NAME:
            shared_secrets[secret.key] = secret

    if secret_type == PERSONAL_SECRET_TYPE_NAME:
        for secret in secrets:
            if secret.key in personal_secrets:
                secrets_to_return_map[secret.key] = personal_secrets[secret.key]
            else:
                if secret.key not in secrets_to_return_map:
                    secrets_to_return_map[secret.key] = secret
    elif secret_type == SHARED_SECRET_TYPE_NAME:
        for secret in secrets:
            if secret.key in shared_secrets:
                secrets_to_return_map[secret.key] = shared_secrets[secret.key]
            else:
                if secret.key not in secrets_to_return_map:
                    secrets_to_return_map[secret.key] = secret

    for secret in secrets_to_return_map.values():
        secrets_to_return.append(secret)

    return secrets_to_return


def substitute_secrets(
    secrets: List[SingleEnvironmentVariable],
) -> List[SingleEnvironmentVariable]:
    hashmap_of_complete_variables: Dict[str, str] = {}
    hashmap_of_self_refs: Dict[str, str] = {}
    expanded_secrets: List[SingleEnvironmentVariable] = []

    for secret in secrets:
        expanded_variable = get_expanded_env_variable(
            secrets, secret.key, hashmap_of_complete_variables, hashmap_of_self_refs
        )

        secret_copy = secret.copy(deep=True)
        secret_copy.value = expanded_variable
        expanded_secrets.append(secret_copy)

    return expanded_secrets


def get_expanded_env_variable(
    secrets: List[SingleEnvironmentVariable],
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
                expanded_variable_value = get_expanded_env_variable(
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


def filter_reserved_env_vars(env: Dict[str, SingleEnvironmentVariable]) -> None:
    for reserved_env_name in RESERVED_ENV_VARS:
        if reserved_env_name in env:
            del env[reserved_env_name]
            print("Reserved name!")
    for reserved_env_prefix in RESERVED_ENV_VAR_PREFIXES:
        for env_name in env.keys():
            if env_name.startswith(reserved_env_prefix):
                del env[env_name]
                print("Reserved prefix!")
