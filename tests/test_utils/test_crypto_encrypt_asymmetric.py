import pytest
from infisical.utils.crypto import decrypt_asymmetric, encrypt_asymmetric

BOB_PRIVATE_KEY = b"rMZ\xd8v\xfc\xdchn_\xb3\xf3\xb6(@\xb5\x15F\xdf\x12\x13\xf6_\x827\xea\x8eBc\x1fQ\x9b"
BOB_PUBLIC_KEY = (
    b"D5:\x10\x82\xdasTz4\xb7\x13\xd0C\xcaM%\xdbBl\x81\xe5\xba\xb8i)\xaa\x1c\xbc=Nl"
)
BOB_PRIVATE_KEY_B64 = "ck1a2Hb83GhuX7PztihAtRVG3xIT9l+CN+qOQmMfUZs="
BOB_PUBLIC_KEY_B64 = "RDU6EILac1R6NLcT0EPKTSXbQmyB5bq4aSmqHLw9Tmw="

ALICE_PRIVATE_KEY = b"\xe5{g\xe1\xcb\xb2\xbfT{\xd9\x96\xdc\x80-\x991\r\xb4Z\x13}\xef\x8c\xdc'\x89x\xd1\x0c\xe4<\x04"
ALICE_PUBLIC_KEY = (
    b"\x0f%*\x83\xb8\\N}R\xaa\xcd;\x021\xd9J\xae\xf4G$>\x17\xff\x01\xc3\xd2\xbaQ11\x04Z"
)
ALICE_PRIVATE_KEY_B64 = "5Xtn4cuyv1R72ZbcgC2ZMQ20WhN974zcJ4l40QzkPAQ="
ALICE_PUBLIC_KEY_B64 = "DyUqg7hcTn1Sqs07AjHZSq70RyQ+F/8Bw9K6UTExBFo="


def test_encrypt_asymmetric_base64() -> None:
    ciphertext, nonce = encrypt_asymmetric(
        plaintext="Hello World!",
        private_key=BOB_PRIVATE_KEY_B64,
        public_key=ALICE_PUBLIC_KEY_B64,
    )

    plaintext = decrypt_asymmetric(
        ciphertext=ciphertext,
        nonce=nonce,
        private_key=ALICE_PRIVATE_KEY_B64,
        public_key=BOB_PUBLIC_KEY_B64,
    )

    assert plaintext == "Hello World!"


def test_encrypt_asymmetric_bytes() -> None:
    ciphertext, nonce = encrypt_asymmetric(
        plaintext=b"Hello World!",
        private_key=BOB_PRIVATE_KEY,
        public_key=ALICE_PUBLIC_KEY,
    )

    plaintext = decrypt_asymmetric(
        ciphertext=ciphertext,
        nonce=nonce,
        private_key=ALICE_PRIVATE_KEY,
        public_key=BOB_PUBLIC_KEY,
    )

    assert plaintext == "Hello World!"


def test_encrypt_asymmetric_empty_param() -> None:
    cipher, nonce = encrypt_asymmetric(
        plaintext="", private_key=ALICE_PRIVATE_KEY, public_key=BOB_PUBLIC_KEY
    )

    assert len(cipher) > 0
    assert len(nonce) > 0

    with pytest.raises(ValueError):
        encrypt_asymmetric(
            plaintext="Hello World!", private_key="", public_key=BOB_PUBLIC_KEY
        )

    with pytest.raises(ValueError):
        encrypt_asymmetric(
            plaintext="Hello World!", private_key=ALICE_PRIVATE_KEY, public_key=""
        )
