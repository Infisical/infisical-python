import pytest
from infisical.utils.crypto import decrypt_symmetric


def test_decrypt_symmetric_base64() -> None:
    plaintext = decrypt_symmetric(
        key="NDQxYThhNGFlOTdlMDQyNzBmOWI0MDkyZDgzYThmMGQ=",
        ciphertext="6ggRNtwCS58YBk8YoOQBTX0Y9Em/jY5BjJDrf8OseFU=",
        tag="DlHIpSGeE7FIJQ3bxyqB7Q==",
        iv="H/cRvADtxDa4XWzM2p1j0w==",
    )

    assert plaintext == "9c07298c06c6aaa762fcee342cf6bc34"


def test_decrypt_symmetric_bytes() -> None:
    plaintext = decrypt_symmetric(
        key=b"441a8a4ae97e04270f9b4092d83a8f0d",
        ciphertext=b"\xea\x08\x116\xdc\x02K\x9f\x18\x06O\x18\xa0\xe4\x01M}\x18\xf4I\xbf\x8d\x8eA\x8c\x90\xeb\x7f\xc3\xacxU",
        tag=b"\x0eQ\xc8\xa5!\x9e\x13\xb1H%\r\xdb\xc7*\x81\xed",
        iv=b"\x1f\xf7\x11\xbc\x00\xed\xc46\xb8]l\xcc\xda\x9dc\xd3",
    )

    assert plaintext == "9c07298c06c6aaa762fcee342cf6bc34"


def test_decrypt_symmetric_empty_param() -> None:
    with pytest.raises(ValueError):
        decrypt_symmetric(
            key="",
            ciphertext="6ggRNtwCS58YBk8YoOQBTX0Y9Em/jY5BjJDrf8OseFU=",
            tag="DlHIpSGeE7FIJQ3bxyqB7Q==",
            iv="H/cRvADtxDa4XWzM2p1j0w==",
        )

    with pytest.raises(ValueError):
        decrypt_symmetric(
            key="NDQxYThhNGFlOTdlMDQyNzBmOWI0MDkyZDgzYThmMGQ=",
            ciphertext="6ggRNtwCS58YBk8YoOQBTX0Y9Em/jY5BjJDrf8OseFU=",
            tag="",
            iv="H/cRvADtxDa4XWzM2p1j0w==",
        )

    with pytest.raises(ValueError):
        decrypt_symmetric(
            key="NDQxYThhNGFlOTdlMDQyNzBmOWI0MDkyZDgzYThmMGQ=",
            ciphertext="6ggRNtwCS58YBk8YoOQBTX0Y9Em/jY5BjJDrf8OseFU=",
            tag="DlHIpSGeE7FIJQ3bxyqB7Q==",
            iv="",
        )

    decrypt_symmetric(
        key="C4AmL9liaUXm5tNVoHBTJw==",
        ciphertext="",
        tag="w+3JZYTW+YiKagCseraf4Q==",
        iv="zw8vhOL67bEhvRijTCA+vA==",
    )
