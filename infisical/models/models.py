from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from typing_extensions import Literal


class Secret(BaseModel):
    id: str = Field(..., alias="_id")
    version: int
    workspace: str
    type: Literal["shared", "personal"]
    environment: str
    secret_key_ciphertext: str = Field(..., alias="secretKeyCiphertext")
    secret_key_iv: str = Field(..., alias="secretKeyIV")
    secret_key_tag: str = Field(..., alias="secretKeyTag")
    secret_value_ciphertext: str = Field(..., alias="secretValueCiphertext")
    secret_value_iv: str = Field(..., alias="secretValueIV")
    secret_value_tag: str = Field(..., alias="secretValueTag")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    user: Optional[str] = None


class SecretBundle(BaseModel):
    secret_name: str
    secret_value: Optional[str] = None
    version: Optional[int] = None
    workspace: Optional[str] = None
    environment: Optional[str] = None
    type: Optional[Literal["shared", "personal"]] = None
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    is_fallback: bool = False
    last_fetched_at: datetime = Field(default_factory=datetime.now)


class ServiceTokenData(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    workspace: str
    environment: str
    user: str
    service_account: str
    last_used: datetime = Field()
    expires_at: datetime = Field(..., alias="expiresAt")
    encrypted_key: str = Field(..., alias="encryptedKey")
    iv: str
    tag: str
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
