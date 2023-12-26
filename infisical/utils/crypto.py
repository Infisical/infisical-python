from base64 import b64decode, b64encode
from typing import Tuple, Union

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from nacl import public, utils

Base64String = str
Buffer = Union[bytes, bytearray, memoryview]


def encrypt_asymmetric(
    plaintext: Union[Buffer, str],
    public_key: Union[Buffer, Base64String, public.PublicKey],
    private_key: Union[Buffer, Base64String, public.PrivateKey],
) -> Tuple[Base64String, Base64String]:
    """Performs asymmetric encryption of the ``plaintext`` with x25519-xsalsa20-poly1305
    algorithm with the given parameters. Each of those params should be either the raw value in bytes
    or a base64 string.

    :param plaintext: The text to encrypt
    :param public_key: The public key
    :param private_key: The private key
    :raises ValueError: If ``plaintext``, ``public_key`` or ``private_key`` are empty
    :return: A tuple containing the ciphered text and the random nonce used for encryption
    """
    if (not isinstance(public_key, public.PublicKey) and len(public_key) == 0) or (
        not isinstance(private_key, public.PrivateKey) and len(private_key) == 0
    ):
        raise ValueError("Public key and private key cannot be empty!")

    m_plaintext = (
        str.encode(plaintext, "utf-8") if isinstance(plaintext, str) else plaintext
    )
    m_public_key = (
        b64decode(public_key) if isinstance(public_key, Base64String) else public_key
    )
    m_public_key = (
        public.PublicKey(m_public_key)
        if isinstance(m_public_key, (bytes, bytearray, memoryview))
        else m_public_key
    )
    m_private_key = (
        b64decode(private_key) if isinstance(private_key, Base64String) else private_key
    )
    m_private_key = (
        public.PrivateKey(m_private_key)
        if isinstance(m_private_key, (bytes, bytearray, memoryview))
        else m_private_key
    )

    nonce = utils.random(24)
    box = public.Box(m_private_key, m_public_key)
    ciphertext = box.encrypt(m_plaintext, nonce).ciphertext

    return (b64encode(ciphertext).decode("utf-8"), b64encode(nonce).decode("utf-8"))


def decrypt_asymmetric(
    ciphertext: Union[Buffer, Base64String],
    nonce: Union[Buffer, Base64String],
    public_key: Union[Buffer, Base64String, public.PublicKey],
    private_key: Union[Buffer, Base64String, public.PrivateKey],
) -> str:
    """Performs asymmetric decryption of the ``ciphertext`` with x25519-xsalsa20-poly1305
    algorithm with the given parameters. Each of those params should be either the raw value in bytes
    or a base64 string.

    :param ciphertext: The ciphered text to decrypt
    :param nonce: The nonce used for encryption
    :param public_key: The public key
    :param private_key: The private key
    :raises ValueError: If ``ciphertext``, ``nonce``, ``public_key`` or ``private_key`` are empty
    :return: The deciphered text
    """
    if (
        len(ciphertext) == 0
        or len(nonce) == 0
        or (not isinstance(public_key, public.PublicKey) and len(public_key) == 0)
        or (not isinstance(private_key, public.PrivateKey) and len(private_key) == 0)
    ):
        raise ValueError(
            "Public key, private key, ciphertext and nonce cannot be empty!"
        )

    m_ciphertext = (
        b64decode(ciphertext) if isinstance(ciphertext, Base64String) else ciphertext
    )
    m_nonce = b64decode(nonce) if isinstance(nonce, Base64String) else nonce
    m_public_key = (
        b64decode(public_key) if isinstance(public_key, Base64String) else public_key
    )
    m_public_key = (
        public.PublicKey(m_public_key)
        if isinstance(m_public_key, (bytes, bytearray, memoryview))
        else m_public_key
    )
    m_private_key = (
        b64decode(private_key) if isinstance(private_key, Base64String) else private_key
    )
    m_private_key = (
        public.PrivateKey(m_private_key)
        if isinstance(m_private_key, (bytes, bytearray, memoryview))
        else m_private_key
    )

    box = public.Box(m_private_key, m_public_key)
    plaintext = box.decrypt(m_ciphertext, m_nonce)

    return plaintext.decode("utf-8")


def create_symmetric_key_helper() -> str:
    return b64encode(get_random_bytes(32)).decode("utf-8")


def encrypt_symmetric_helper(
    plaintext: str, key: Base64String
) -> Tuple[Base64String, Base64String, Base64String]:
    IV_BYTES_SIZE = 12
    iv = get_random_bytes(IV_BYTES_SIZE)

    cipher = AES.new(b64decode(key), AES.MODE_GCM, nonce=iv)

    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode("utf-8"))

    return (
        b64encode(ciphertext).decode("utf-8"),
        b64encode(iv).decode("utf-8"),
        b64encode(tag).decode("utf-8"),
    )


def decrypt_symmetric_helper(
    ciphertext: Base64String, key: Base64String, iv: Base64String, tag: Base64String
) -> str:
    cipher = AES.new(b64decode(key), AES.MODE_GCM, nonce=b64decode(iv))
    plaintext = cipher.decrypt_and_verify(b64decode(ciphertext), b64decode(tag))

    return plaintext.decode("utf-8")


def encrypt_symmetric_128_bit_hex_key_utf8(
    plaintext: str, key: str
) -> Tuple[Base64String, Base64String, Base64String]:
    """Encrypts the ``plaintext`` with aes-256-gcm using the given ``key``.
    The key should be either the raw value in bytes or a base64 string.

    :param plaintext: text to encrypt
    :param key: UTF-8, 128-bit AES key used for encryption
    :raises ValueError: If either ``plaintext`` or ``key`` is empty
    :return: Ciphered text
    """
    if len(key) == 0:
        raise ValueError("The given key is empty!")

    BLOCK_SIZE_BYTES = 16

    iv = get_random_bytes(BLOCK_SIZE_BYTES)
    cipher = AES.new(bytes(key, "utf-8"), AES.MODE_GCM, nonce=iv)

    ciphertext, tag = cipher.encrypt_and_digest(str.encode(plaintext, "utf-8"))

    return (
        b64encode(ciphertext).decode("utf-8"),
        b64encode(iv).decode("utf-8"),
        b64encode(tag).decode("utf-8"),
    )


def decrypt_symmetric_128_bit_hex_key_utf8(
    key: str, ciphertext: Base64String, tag: Base64String, iv: Base64String
) -> str:
    """Decrypts the ``ciphertext`` with aes-256-gcm using ``iv``, ``tag``
    and ``key``.

    :param key: UTF-8, 128-bit hex AES key
    :param ciphertext: base64 ciphered text to decrypt
    :param tag: base64 tag/mac used for verification
    :param iv: base64 nonce
    :raises ValueError: If ``ciphertext``, ``iv``, ``tag`` or ``key`` are empty or tag/mac does not match
    :return: Deciphered text
    """
    if len(tag) == 0 or len(iv) == 0 or len(key) == 0:
        raise ValueError("One of the given parameter is empty!")

    try:
        key_buffer = bytes(key, "utf-8")
        iv_decoded = b64decode(iv)
        tag_decoded = b64decode(tag)
        ciphertext_decoded = b64decode(ciphertext)

        cipher = AES.new(key_buffer, AES.MODE_GCM, nonce=iv_decoded)
        plaintext = cipher.decrypt_and_verify(ciphertext_decoded, tag_decoded)

        return plaintext.decode("utf-8")
    except ValueError as err:
        raise ValueError("Incorrect decryption or MAC check failed") from err
