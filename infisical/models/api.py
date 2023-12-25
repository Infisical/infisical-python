from typing import List, Optional

from infisical.models.models import Secret
from pydantic import BaseModel
from typing_extensions import Literal


class GetSecretsDTO(BaseModel):
    workspace_id: str
    environment: str
    path: str
    include_imports: bool


class GetSecretDTO(BaseModel):
    secret_name: str
    workspace_id: str
    environment: str
    type: Literal["shared", "personal"]
    path: str


class CreateSecretDTO(BaseModel):
    secret_name: str
    workspace_id: str
    environment: str
    type: Literal["shared", "personal"]
    path: str
    secret_key_ciphertext: str
    secret_key_iv: str
    secret_key_tag: str
    secret_value_ciphertext: str
    secret_value_iv: str
    secret_value_tag: str


class UpdateSecretDTO(BaseModel):
    secret_name: str
    workspace_id: str
    environment: str
    type: Literal["shared", "personal"]
    path: str
    secret_value_ciphertext: str
    secret_value_iv: str
    secret_value_tag: str


class DeleteSecretDTO(BaseModel):
    secret_name: str
    workspace_id: str
    environment: str
    type: Literal["shared", "personal"]
    path: str


class SecretImport(BaseModel):
    secretPath: str
    folderId: str
    environment: str
    secrets: List[Secret]

class SecretsResponse(BaseModel):
    secrets: List[Secret]
    imports: Optional[List[SecretImport]] = None


class SecretResponse(BaseModel):
    secret: Secret
