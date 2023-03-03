from Cryptodome.Cipher import AES


def decrypt_symmetric(key: bytes, cipher_text: bytes, tag: bytes, iv: bytes) -> bytes:
    if len(cipher_text) == 0 and len(tag) == 0 and len(iv) == 0:
        raise ValueError()

    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)

    return cipher.decrypt_and_verify(cipher_text, tag)
