import datetime
from typing import List

from pydantic import BaseModel, Field


class GetServiceTokenDetailsUserResponse(BaseModel):
    id: str = Field(..., alias="_id")
    email: str
    created_at: datetime.datetime = Field(..., alias="createdAt")
    updated_at: datetime.datetime = Field(..., alias="updatedAt")
    v: int = Field(..., alias="__v")
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")


class GetServiceTokenDetailsResponse(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    workspace: str
    environment: str
    user: GetServiceTokenDetailsUserResponse
    expires_at: datetime.datetime = Field(..., alias="expiresAt")
    encrypted_key: str = Field(..., alias="encryptedKey")
    iv: str
    tag: str
    created_at: datetime.datetime = Field(..., alias="createdAt")
    updated_at: datetime.datetime = Field(..., alias="updatedAt")
    v: int = Field(..., alias="__v")


class GetEncryptedSecretsV2Request(BaseModel):
    environment: str
    workspace_id: str = Field(..., alias="workspaceId")
    tag_slugs: str = Field("", alias="tagSlugs")


class GetEncryptedSecretsV2TagResponse(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    slug: str
    workspace: str


class GetEncryptedSecretsV2SecretResponse(BaseModel):
    id: str = Field(..., alias="_id")
    version: int
    workspace: str
    type: str
    environment: str
    secret_key_ciphertext: str = Field(..., alias="secretKeyCiphertext")
    secret_key_iv: str = Field(..., alias="secretKeyIV")
    secret_key_tag: str = Field(..., alias="secretKeyTag")
    secret_value_ciphertext: str = Field(..., alias="secretValueCiphertext")
    secret_value_iv: str = Field(..., alias="secretValueIV")
    secret_value_tag: str = Field(..., alias="secretValueTag")
    secret_comment_ciphertext: str = Field(..., alias="secretCommentCiphertext")
    secret_comment_iv: str = Field(..., alias="secretCommentIV")
    secret_comment_tag: str = Field(..., alias="secretCommentTag")
    v: int = Field(..., alias="__v")
    created_at: datetime.datetime = Field(..., alias="createdAt")
    updated_at: datetime.datetime = Field(..., alias="updatedAt")
    user: str = ""
    tags: List[GetEncryptedSecretsV2TagResponse]


class GetEncryptedSecretsV2Response(BaseModel):
    secrets: List[GetEncryptedSecretsV2SecretResponse]
