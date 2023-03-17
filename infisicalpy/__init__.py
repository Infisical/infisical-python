from typing import Optional

from infisicalpy.constants import INFISICAL_URL

from .client.infisicalclient import InfisicalClient

_global_instance: Optional[InfisicalClient] = None


def connect(
    token: str,
    site_url: str = INFISICAL_URL,
    attach_to_process_env: bool = False,
    debug: bool = False,
) -> InfisicalClient:
    """Connect to infisical and pre-fetch secrets. This method store the :class:`InfisicalClient`
    instance in a global variable that will be available in other modules.

    :param token: The service token to be used to fetch secrets
    :param site_url: The domain on the infisical API to use, defaults to the cloud one
    :param attach_to_process_env: Inject the secrets in `os.environ`, defaults to False
    :param debug: Display error messages, defaults to False
    :return: The global :class:`InfisicalClient` instance
    """
    instance = InfisicalClient.connect(token, site_url, attach_to_process_env, debug)

    global _global_instance
    _global_instance = instance

    return instance


def create_connection(
    token: str,
    site_url: str = INFISICAL_URL,
    debug: bool = False,
) -> InfisicalClient:
    """Connect to infisical and pre-fetch secrets.

    :param token: The service token to be used to fetch secrets
    :param site_url: The domain on the infisical API to use, defaults to the cloud one
    :param debug: Display error messages, defaults to False
    :return: A :class:`InfisicalClient` instance
    """
    instance = InfisicalClient.connect(token=token, site_url=site_url, debug=debug)

    return instance


def get(key: str) -> Optional[str]:
    """Retrieve a secret value from `key` if found from the global instance created
    with `connect()`.

    :param key: The key of the secret to retrieve
    :return: The key or None if secret is not found or if `connect()` was never called
    """
    if _global_instance is not None:
        return _global_instance.get(key)

    return None
