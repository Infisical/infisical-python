from typing import Dict, Optional

from pydantic import BaseModel
from requests import Session
from typing_extensions import Literal


class WorkspaceConfig(BaseModel):
    workspace_id: str
    environment: str
    workspace_key: str


class ClientConfig(BaseModel):
    auth_mode: Literal["service_token"]
    credentials: Dict[Literal["service_token_key"], str]
    workspace_config: Optional[WorkspaceConfig]
    cache_ttl: int
