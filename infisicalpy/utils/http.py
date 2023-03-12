from typing import Any, Optional, Union
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

DEFAULT_TIMEOUT = 40  # seconds


class BaseUrlSession(requests.Session):
    base_url = ""

    def __init__(self, base_url: Optional[str] = None) -> None:
        if base_url:
            self.base_url = base_url
        super().__init__()

    def request(
        self,
        method: Union[str, bytes],
        url: Any,
        *args: Any,
        **kwargs: Any,
    ) -> requests.Response:
        url = self.create_url(url)
        return super().request(method, url, *args, **kwargs)

    def prepare_request(self, request: requests.Request) -> requests.PreparedRequest:
        request.url = self.create_url(request.url)
        return super().prepare_request(request)

    def create_url(self, url: str) -> str:
        return urljoin(self.base_url, url)


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


def get_http_client(
    base_url: Optional[str],
    retries: int = 3,
    backoff_factor: int = 1,
    timeout: int = DEFAULT_TIMEOUT,
) -> BaseUrlSession:
    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = TimeoutHTTPAdapter(max_retries=retry_strategy, timeout=timeout)

    http = BaseUrlSession(base_url=base_url)
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    return http
