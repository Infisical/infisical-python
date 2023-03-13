import pytest
from infisicalpy.utils.crypto import decrypt_asymmetric

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


def test_decrypt_asymmetric_base64() -> None:
    plaintext = decrypt_asymmetric(
        ciphertext="m9Woltk3alznKDFbgwhe8JpFb9B+vI5CtIDvng==",
        public_key=BOB_PUBLIC_KEY_B64,
        private_key=ALICE_PRIVATE_KEY_B64,
        nonce="fghal5SodvyeM4L2r5EEStSI9xfPx7LH",
    )

    assert plaintext == "Hello World!"


def test_decrypt_asymmetric_bytes() -> None:
    plaintext = decrypt_asymmetric(
        ciphertext=b"\x9b\xd5\xa8\x96\xd97j\\\xe7(1[\x83\x08^\xf0\x9aEo\xd0~\xbc\x8eB\xb4\x80\xef\x9e",
        public_key=BOB_PUBLIC_KEY,
        private_key=ALICE_PRIVATE_KEY,
        nonce=b"~\x08Z\x97\x94\xa8v\xfc\x9e3\x82\xf6\xaf\x91\x04J\xd4\x88\xf7\x17\xcf\xc7\xb2\xc7",
    )

    assert plaintext == "Hello World!"


def test_decrypt_asymmetric_empty_param() -> None:
    with pytest.raises(ValueError):
        decrypt_asymmetric(
            ciphertext="",
            public_key=BOB_PUBLIC_KEY_B64,
            private_key=ALICE_PRIVATE_KEY_B64,
            nonce="fghal5SodvyeM4L2r5EEStSI9xfPx7LH",
        )

    with pytest.raises(ValueError):
        decrypt_asymmetric(
            ciphertext="m9Woltk3alznKDFbgwhe8JpFb9B+vI5CtIDvng==",
            public_key="",
            private_key=ALICE_PRIVATE_KEY_B64,
            nonce="fghal5SodvyeM4L2r5EEStSI9xfPx7LH",
        )

    with pytest.raises(ValueError):
        decrypt_asymmetric(
            ciphertext="m9Woltk3alznKDFbgwhe8JpFb9B+vI5CtIDvng==",
            public_key=BOB_PUBLIC_KEY_B64,
            private_key="",
            nonce="fghal5SodvyeM4L2r5EEStSI9xfPx7LH",
        )

    with pytest.raises(ValueError):
        decrypt_asymmetric(
            ciphertext="m9Woltk3alznKDFbgwhe8JpFb9B+vI5CtIDvng==",
            public_key=BOB_PUBLIC_KEY_B64,
            private_key=ALICE_PRIVATE_KEY_B64,
            nonce="",
        )
