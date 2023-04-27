from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Union

from typing_extensions import Literal

if TYPE_CHECKING:
    from infisical import InfisicalClient

from infisical.logger import logger
from infisical.models.models import SecretBundle
from infisical.services.secret_service import SecretService


def get_all_secrets_helper(instance: "InfisicalClient"):
    try:
        if not instance.client_config:
            raise Exception("Failed to find client config")

        if not instance.client_config.workspace_config:
            instance.client_config.workspace_config = (
                SecretService.populate_client_config(
                    api_request=instance.api_request,
                    client_config=instance.client_config,
                )
            )

        secret_bundles = SecretService.get_decrypted_secrets(
            api_request=instance.api_request,
            workspace_id=instance.client_config.workspace_config.workspace_id,
            environment=instance.client_config.workspace_config.environment,
            workspace_key=instance.client_config.workspace_config.workspace_key,
        )

        for secret_bundle in secret_bundles:
            cache_key = f"{secret_bundle.type}-{secret_bundle.secret_name}"
            instance.cache[cache_key] = secret_bundle

        return secret_bundles
    except Exception as exc:
        if instance.debug:
            logger.exception(exc)

    return [SecretService.get_fallback_secret(secret_name="")]


def get_secret_helper(
    instance: "InfisicalClient", secret_name: str, type: Literal["shared", "personal"]
):
    cache_key = f"{type}-{secret_name}"
    cached_secret: Union[SecretBundle, None] = None
    try:
        if not instance.client_config:
            raise Exception("Failed to find client config")

        if not instance.client_config.workspace_config:
            instance.client_config.workspace_config = (
                SecretService.populate_client_config(
                    api_request=instance.api_request,
                    client_config=instance.client_config,
                )
            )

        cached_secret = instance.cache.get(cache_key)

        if cached_secret:
            current_time = datetime.now()
            cache_expiry_time = cached_secret.last_fetched_at + timedelta(
                seconds=instance.client_config.cache_ttl
            )

            if current_time < cache_expiry_time:
                if instance.debug:
                    print(f"Returning cached secret: {cached_secret.secret_name}")

                return cached_secret

        secret_bundle = SecretService.get_decrypted_secret(
            api_request=instance.api_request,
            secret_name=secret_name,
            workspace_id=instance.client_config.workspace_config.workspace_id,
            environment=instance.client_config.workspace_config.environment,
            workspace_key=instance.client_config.workspace_config.workspace_key,
            type=type,
        )

        instance.cache[secret_name] = secret_bundle

        return secret_bundle

    except Exception as exc:
        if instance.debug:
            logger.exception(exc)

        if cached_secret:
            if instance.debug:
                print(f"Returning cached secret: {cached_secret}")

            return cached_secret

    return SecretService.get_fallback_secret(secret_name=secret_name)


def create_secret_helper(
    instance: "InfisicalClient",
    secret_name: str,
    secret_value: str,
    type: Literal["shared", "personal"],
):
    try:
        if not instance.client_config:
            raise Exception("Failed to find client config")

        if not instance.client_config.workspace_config:
            instance.client_config.workspace_config = (
                SecretService.populate_client_config(
                    api_request=instance.api_request,
                    client_config=instance.client_config,
                )
            )

        secret_bundle = SecretService.create_secret(
            api_request=instance.api_request,
            secret_name=secret_name,
            secret_value=secret_value,
            workspace_id=instance.client_config.workspace_config.workspace_id,
            environment=instance.client_config.workspace_config.environment,
            workspace_key=instance.client_config.workspace_config.workspace_key,
            type=type,
        )

        cache_key = f"{type}-{secret_name}"
        instance.cache[cache_key] = secret_bundle

        return secret_bundle
    except Exception as exc:
        if instance.debug:
            logger.exception(exc)

    return SecretService.get_fallback_secret(secret_name=secret_name)


def update_secret_helper(
    instance: "InfisicalClient",
    secret_name: str,
    secret_value: str,
    type: Literal["shared", "personal"],
):
    try:
        if not instance.client_config:
            raise Exception("Failed to find client config")

        if not instance.client_config.workspace_config:
            instance.client_config.workspace_config = (
                SecretService.populate_client_config(
                    api_request=instance.api_request,
                    client_config=instance.client_config,
                )
            )

        secret_bundle = SecretService.update_secret(
            api_request=instance.api_request,
            secret_name=secret_name,
            secret_value=secret_value,
            workspace_id=instance.client_config.workspace_config.workspace_id,
            environment=instance.client_config.workspace_config.environment,
            workspace_key=instance.client_config.workspace_config.workspace_key,
            type=type,
        )

        cache_key = f"{type}-{secret_name}"
        instance.cache[cache_key] = secret_bundle

        return secret_bundle
    except Exception as exc:
        if instance.debug:
            logger.exception(exc)

    return SecretService.get_fallback_secret(secret_name=secret_name)


def delete_secret_helper(
    instance: "InfisicalClient", secret_name: str, type: Literal["shared", "personal"]
):
    try:
        if not instance.client_config:
            raise Exception("Failed to find client config")

        if not instance.client_config.workspace_config:
            instance.client_config.workspace_config = (
                SecretService.populate_client_config(
                    api_request=instance.api_request,
                    client_config=instance.client_config,
                )
            )

        secret_bundle = SecretService.delete_secret(
            api_request=instance.api_request,
            secret_name=secret_name,
            workspace_id=instance.client_config.workspace_config.workspace_id,
            environment=instance.client_config.workspace_config.environment,
            workspace_key=instance.client_config.workspace_config.workspace_key,
            type=type,
        )

        cache_key = f"{type}-{secret_name}"
        instance.cache[cache_key] = secret_bundle

        return secret_bundle
    except Exception as exc:
        if instance.debug:
            logger.exception(exc)

    return SecretService.get_fallback_secret(secret_name=secret_name)
