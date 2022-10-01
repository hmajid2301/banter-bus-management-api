from enum import Enum

from beanie import Document, Indexed
from pydantic import BaseModel

from app.core.models import QuestionGroup


class QuestionIDsPagination(BaseModel):
    question_ids: list[str]
    cursor: str | None = None


class Question(Document):
    question_id: Indexed(str, unique=True)  # type: ignore
    game_name: str
    round_: str | None
    enabled: bool = True
    content: dict[str, str]
    group: QuestionGroup | None = None

    class Config:
        allow_population_by_field_name = True
        fields = {"round_": "round"}

    class Collection:
        name = "question"


class QuestionTranslation(BaseModel):
    question_id: str
    game_name: str
    round_: str | None
    language_code: str
    enabled: bool = True
    content: str
    group: QuestionGroup | None = None

    class Config:
        allow_population_by_field_name = True
        fields = {"round_": "round"}


class NewQuestion(BaseModel):
    game_name: str
    round_: str | None
    content: str
    language_code: str = "en"
    group: QuestionGroup | None = None

    class Config:
        allow_population_by_field_name = True
        fields = {"round_": "round"}


class QuestionType(str, Enum):
    answer = "answer"
    question = "question"


class QuestionSimple(BaseModel):
    question_id: str
    content: str
    type_: str

    class Config:
        allow_population_by_field_name = True
        fields = {"type_": "type"}
