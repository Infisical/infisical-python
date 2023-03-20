import re

INFISICAL_URL = "https://app.infisical.com"

SERVICE_TOKEN_REGEX = re.compile(r"(st\.[a-f0-9]+\.[a-f0-9]+)\.([a-f0-9]+)")
