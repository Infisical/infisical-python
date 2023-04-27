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
