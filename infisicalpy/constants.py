from typing import List

INFISICAL_DEFAULT_API_URL = "https://app.infisical.com/api"
INFISICAL_TOKEN_NAME = "INFISICAL_TOKEN"
INFISICAL_API_URL_NAME = "INFISICAL_API_URL"

SECRET_TYPE_PERSONAL = "personal"
SECRET_TYPE_SHARED = "shared"
PERSONAL_SECRET_TYPE_NAME = "personal"
SHARED_SECRET_TYPE_NAME = "shared"


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
