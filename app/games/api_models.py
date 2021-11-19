from pydantic import BaseModel


class GameIn(BaseModel):
    name: str
    display_name: str
    description: str
    rules_url: str


class GameOut(BaseModel):
    name: str
    display_name: str
    description: str
    enabled: bool
    rules_url: str
