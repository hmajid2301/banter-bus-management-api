from typing import Any, Optional

from pydantic import BaseModel


class StoryIn(BaseModel):
    game_name: str
    question: str
    round: Optional[str]
    nickname: Optional[str]
    answers: Any


class StoryOut(BaseModel):
    id: str
    game_name: str
    question: str
    round: Optional[str] = None
    nickname: Optional[str] = None
    answers: Any
