from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

DEFAULT_TIMEOUT = 40  # seconds


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(
        self, request: requests.PreparedRequest, *args: Any, **kwargs: Any
    ) -> requests.Response:
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, *args, **kwargs)


def get_client(
    retries: int = 3, backoff_factor: int = 1, timeout: int = DEFAULT_TIMEOUT
) -> requests.Session:
    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = TimeoutHTTPAdapter(max_retries=retry_strategy, timeout=timeout)

    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    return http
