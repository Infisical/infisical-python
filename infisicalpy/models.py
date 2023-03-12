from pydantic import BaseModel


class InfisicalSecret(BaseModel):
    key: str
    value: str
    type: str
