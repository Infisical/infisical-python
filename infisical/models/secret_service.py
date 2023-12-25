from typing import Dict, Optional, Union

from pydantic import BaseModel
from requests import Session
from typing_extensions import Literal

class WorkspaceConfig(BaseModel):
    workspace_id: str
    workspace_key: str

class ServiceTokenCredentials(BaseModel):
    service_token_key: str

class ServiceTokenV3Credentials(BaseModel):
    public_key: str
    private_key: str

class ClientConfig(BaseModel):
    auth_mode: Literal["service_token", "service_token_v3"]
    credentials: Union[ServiceTokenCredentials, ServiceTokenV3Credentials]
    workspace_config: Optional[WorkspaceConfig] = None
    cache_ttl: int
