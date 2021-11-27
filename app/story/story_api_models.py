from typing import List, Optional, Union

from pydantic import BaseModel

from app.core.models import CaertsianCoordinateColor


class FibbingItAnswer(BaseModel):
    nickname: str
    answer: str


class QuiblyAnswer(BaseModel):
    nickname: str
    answer: str
    votes: int


class StoryIn(BaseModel):
    game_name: str
    question: str
    round: Optional[str]
    nickname: Optional[str]
    answers: Union[List[QuiblyAnswer], List[FibbingItAnswer], List[CaertsianCoordinateColor]]


class StoryOut(BaseModel):
    id: str
    game_name: str
    question: str
    round: Optional[str] = None
    nickname: Optional[str] = None
    answers: Union[List[QuiblyAnswer], List[FibbingItAnswer], List[CaertsianCoordinateColor]]
