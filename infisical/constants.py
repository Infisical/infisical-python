import re

INFISICAL_URL = "https://app.infisical.com"
AUTH_MODE_SERVICE_TOKEN = "service_token"
AUTH_MODE_SERVICE_TOKEN_V3 = "service_token_v3"

SERVICE_TOKEN_REGEX = re.compile(r"(st\.[a-f0-9]+\.[a-f0-9]+)\.([a-f0-9]+)")
