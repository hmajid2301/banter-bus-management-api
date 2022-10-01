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
    round_: str | None
    nickname: str | None
    answers: list[QuiblyAnswer] | list[FibbingItAnswer] | list[CaertsianCoordinateColor]

    class Config:
        allow_population_by_field_name = True
        fields = {"round_": "round"}


class StoryOut(BaseModel):
    story_id: str
    game_name: str
    question: str
    round_: str | None = None
    nickname: str | None = None
    answers: list[QuiblyAnswer] | list[FibbingItAnswer] | list[CaertsianCoordinateColor]

    class Config:
        allow_population_by_field_name = True
        fields = {"round_": "round"}
