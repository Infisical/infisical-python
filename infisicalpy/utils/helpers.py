import base64

from pydantic import BaseModel


class DecodedSymetricEncryptionDetails(BaseModel):
    cipher: bytes
    iv: bytes
    tag: bytes
    key: bytes


def get_base64_decoded_symmetric_encryption_details(
    key: str, cipher: str, iv: str, tag: str
) -> DecodedSymetricEncryptionDetails:
    cihperx = base64.standard_b64decode(cipher)
    keyx = base64.standard_b64decode(key)
    IVx = base64.standard_b64decode(iv)
    tagx = base64.standard_b64decode(tag)

    return DecodedSymetricEncryptionDetails(cipher=cihperx, iv=IVx, tag=tagx, key=keyx)
