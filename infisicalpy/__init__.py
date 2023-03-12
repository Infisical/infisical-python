__version__ = "1.0.0"


from typing import Dict, Optional

from .client.infisicalclient import InfisicalClient

_global_instance: Optional[InfisicalClient] = None


def connect(
    token: str,
    site_url: str,
    attach_to_process_env: bool = False,
    default_values: Optional[Dict[str, str]] = None,
    debug: bool = False,
) -> InfisicalClient:
    instance = InfisicalClient.connect(
        token, site_url, attach_to_process_env, default_values, debug
    )

    _global_instance = instance

    return instance


def create_connection(
    token: str,
    site_url: str,
    default_values: Optional[Dict[str, str]] = None,
    debug: bool = False,
) -> InfisicalClient:
    instance = InfisicalClient.connect(token, site_url, False, default_values, debug)

    return instance


def get_secret_value(key: str) -> Optional[str]:
    if _global_instance:
        return _global_instance.get_secret_value(key)

    return None
