import pytest
from infisicalpy.utils.crypto import decrypt_symmetric, encrypt_symmetric


def test_encrypt_symmetric_base64() -> None:
    ciphertext, iv, tag = encrypt_symmetric(
        plaintext="9c07298c06c6aaa762fcee342cf6bc34",
        key="NDQxYThhNGFlOTdlMDQyNzBmOWI0MDkyZDgzYThmMGQ=",
    )

    plaintext = decrypt_symmetric(
        key="NDQxYThhNGFlOTdlMDQyNzBmOWI0MDkyZDgzYThmMGQ=",
        ciphertext=ciphertext,
        tag=tag,
        iv=iv,
    )

    assert plaintext == "9c07298c06c6aaa762fcee342cf6bc34"


def test_encrypt_symmetric_bytes() -> None:
    ciphertext, iv, tag = encrypt_symmetric(
        plaintext="9c07298c06c6aaa762fcee342cf6bc34",
        key=b"441a8a4ae97e04270f9b4092d83a8f0d",
    )

    plaintext = decrypt_symmetric(
        key="NDQxYThhNGFlOTdlMDQyNzBmOWI0MDkyZDgzYThmMGQ=",
        ciphertext=ciphertext,
        tag=tag,
        iv=iv,
    )

    assert plaintext == "9c07298c06c6aaa762fcee342cf6bc34"


def test_encrypt_symmetric_empty_param() -> None:
    with pytest.raises(ValueError):
        encrypt_symmetric(
            plaintext="",
            key="NDQxYThhNGFlOTdlMDQyNzBmOWI0MDkyZDgzYThmMGQ=",
        )

    with pytest.raises(ValueError):
        encrypt_symmetric(
            plaintext="9c07298c06c6aaa762fcee342cf6bc34",
            key="",
        )
