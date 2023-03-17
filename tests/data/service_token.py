from typing import Any, Dict

from responses import GET, Response, matchers

JSON_SERVICE_TOKEN: Dict[str, Any] = {
    "permissions": ["read"],
    "_id": "63ffd735a54c477c7da0d9bc",
    "name": "test",
    "workspace": "6af866f8a76030530fb57a1f",
    "environment": "dev",
    "user": {
        "_id": "60cf66bab9d37ceabb05ab91",
        "email": "johndoe@example.com",
        "isMfaEnabled": False,
        "mfaMethods": [],
        "devices": [],
        "createdAt": "2023-03-01T14:52:42.860Z",
        "updatedAt": "2023-03-17T13:28:10.870Z",
        "__v": 6,
        "firstName": "John",
        "lastName": "Doe",
    },
    "expiresAt": "2024-02-24T22:52:37.713Z",
    "encryptedKey": "0C200uuKrhqQmc5kvzHrhSlPLxFkMwMy6eSD7dx+zxc=",
    "iv": "c5OE7xqz91OvB/lveFNZyg==",
    "tag": "EmWj3xCEjUjp0Lqmz5anwA==",
    "createdAt": "2023-03-01T22:52:37.715Z",
    "updatedAt": "2023-03-01T22:52:37.715Z",
    "__v": 0,
}

GET_SERVICE_TOKEN_RESPONSE = Response(
    GET,
    "https://infisical.test/api/v2/service-token",
    match=[
        matchers.header_matcher({"Authorization": "Bearer 456"}),
    ],
    json=JSON_SERVICE_TOKEN,
)
