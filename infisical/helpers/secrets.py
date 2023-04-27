from datetime import datetime

from infisical.models.models import Secret, SecretBundle


def transform_secret_to_secret_bundle(
    secret: Secret, secret_name: str, secret_value: str
) -> SecretBundle:
    return SecretBundle(
        secret_name=secret_name,
        secret_value=secret_value,
        version=secret.version,
        workspace=secret.workspace,
        environment=secret.environment,
        type=secret.type,
        updated_at=secret.updated_at,
        created_at=secret.created_at,
        is_fallback=False,
        last_fetched_at=datetime.now(),
    )
