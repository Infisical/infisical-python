from base64 import b64decode, b64encode
from typing import Tuple, Union

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from nacl import public, utils

Base64String = str
Buffer = Union[bytes, bytearray, memoryview]


def encrypt_asymmetric(
    plaintext: Union[Buffer, str],
    public_key: Union[Buffer, Base64String],
    private_key: Union[Buffer, Base64String],
) -> Tuple[Base64String, Base64String]:
    if len(plaintext) == 0 or len(public_key) == 0 or len(private_key) == 0:
        raise ValueError()

    m_plaintext = (
        str.encode(plaintext, "utf-8") if isinstance(plaintext, str) else plaintext
    )
    m_public_key = (
        b64decode(public_key) if isinstance(public_key, Base64String) else public_key
    )
    m_private_key = (
        b64decode(private_key) if isinstance(private_key, Base64String) else private_key
    )

    nonce = utils.random(24)
    box = public.Box(public.PrivateKey(m_private_key), public.PublicKey(m_public_key))
    ciphertext = box.encrypt(m_plaintext, nonce).ciphertext

    return (b64encode(ciphertext).decode("utf-8"), b64encode(nonce).decode("utf-8"))


def decrypt_asymmetric(
    ciphertext: Union[Buffer, Base64String],
    nonce: Union[Buffer, Base64String],
    public_key: Union[Buffer, Base64String],
    private_key: Union[Buffer, Base64String],
) -> str:
    if (
        len(ciphertext) == 0
        or len(nonce) == 0
        or len(public_key) == 0
        or len(private_key) == 0
    ):
        raise ValueError()

    m_ciphertext = (
        b64decode(ciphertext) if isinstance(ciphertext, Base64String) else ciphertext
    )
    m_nonce = b64decode(nonce) if isinstance(nonce, Base64String) else nonce
    m_public_key = (
        b64decode(public_key) if isinstance(public_key, Base64String) else public_key
    )
    m_private_key = (
        b64decode(private_key) if isinstance(private_key, Base64String) else private_key
    )

    box = public.Box(public.PrivateKey(m_private_key), public.PublicKey(m_public_key))
    plaintext = box.decrypt(m_ciphertext, m_nonce)

    return plaintext.decode("utf-8")


def encrypt_symmetric(
    plaintext: Union[Buffer, str], key: Union[Buffer, Base64String]
) -> Tuple[Base64String, Base64String, Base64String]:
    if len(plaintext) == 0 or len(key) == 0:
        raise ValueError()

    BLOCK_SIZE_BYTES = 16

    m_key = b64decode(key) if isinstance(key, Base64String) else key
    m_plaintext = (
        str.encode(plaintext, "utf-8") if isinstance(plaintext, str) else plaintext
    )

    iv = get_random_bytes(BLOCK_SIZE_BYTES)
    cipher = AES.new(m_key, AES.MODE_GCM, nonce=iv)

    cipher_text, tag = cipher.encrypt_and_digest(m_plaintext)

    return (
        b64encode(cipher_text).decode("utf-8"),
        b64encode(iv).decode("utf-8"),
        b64encode(tag).decode("utf-8"),
    )


def decrypt_symmetric(
    key: Union[Buffer, Base64String],
    ciphertext: Union[Buffer, Base64String],
    tag: Union[Buffer, Base64String],
    iv: Union[Buffer, Base64String],
) -> str:
    """Return symmetrically decrypted :ref:`ciphertext` using :ref:`iv`, :ref:`tag`
    and :ref:`key`. Each of those params should be either the raw value in bytes
    or a base64 string.

    :param key: The AES key
    :param ciphertext: The ciphered text to decrypt
    :param tag: The tag/mac used for verification
    :param iv: The nonce
    :raises ValueError: If :ref:`ciphertext`, :ref:`iv` and :ref:`tag` are empty
    :return: Deciphered text
    """
    if len(ciphertext) == 0 or len(tag) == 0 or len(iv) == 0 or len(key) == 0:
        raise ValueError()

    m_key = b64decode(key) if isinstance(key, Base64String) else key
    m_iv = b64decode(iv) if isinstance(iv, Base64String) else iv
    m_ciphertext = (
        b64decode(ciphertext) if isinstance(ciphertext, Base64String) else ciphertext
    )
    m_tag = b64decode(tag) if isinstance(tag, Base64String) else tag

    cipher = AES.new(m_key, AES.MODE_GCM, nonce=m_iv)

    plaintext = cipher.decrypt_and_verify(m_ciphertext, m_tag)

    return plaintext.decode("utf-8")
