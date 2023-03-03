from typing import List

from pydantic import BaseModel, Field


class Tag(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    slug: str
    workspace: str


class SingleEnvironmentVariable(BaseModel):
    key: str
    value: str
    type: str
    id: str = Field(..., alias="_id")
    tags: List[Tag]
    comment: str
