from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class GetServiceTokenDetailsUserResponse(BaseModel):
    id: str = Field(..., alias="id")
    email: str
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    # v: int = Field(..., alias="__v")
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")


class GetServiceTokenDetailsResponse(BaseModel):
    id: str = Field(..., alias="id")
    name: str
    workspace: str = Field(..., alias="projectId")
    user: GetServiceTokenDetailsUserResponse
    expires_at: Optional[datetime] = Field(None, alias="expiresAt")
    encrypted_key: str = Field(..., alias="encryptedKey")
    iv: str
    tag: str
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    #v: int = Field(..., alias="__v")

class KeyData(BaseModel):
    id: str = Field(..., alias="id")
    workspace: str
    encrypted_key: str = Field(..., alias="encryptedKey")
    public_key: str = Field(..., alias="publicKey")
    nonce: str

class GetServiceTokenKeyResponse(BaseModel):
    key: KeyData