from typing import List

INFISICAL_URL = "https://app.infisical.com"
INFISICAL_TOKEN_NAME = "INFISICAL_TOKEN"
INFISICAL_API_URL_NAME = "INFISICAL_API_URL"

SECRET_TYPE_PERSONAL = "personal"
SECRET_TYPE_SHARED = "shared"


RESERVED_ENV_VARS: List[str] = [
    "HOME",
    "PATH",
    "PS1",
    "PS2",
    "PWD",
    "EDITOR",
    "XAUTHORITY",
    "USER",
    "TERM",
    "TERMINFO",
    "SHELL",
    "MAIL",
]

RESERVED_ENV_VAR_PREFIXES: List[str] = ["XDG_", "LC_"]
