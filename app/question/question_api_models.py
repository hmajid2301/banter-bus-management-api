from pydantic import BaseModel

from app.core.models import QuestionGroup
from app.question.question_models import QuestionType


class QuestionIn(BaseModel):
    round_: str | None
    content: str
    language_code: str = "en"
    group: QuestionGroup | None = None

    class Config:
        allow_population_by_field_name = True
        fields = {"round_": "round"}


class QuestionOut(BaseModel):
    question_id: str
    game_name: str
    round_: str | None
    enabled: bool = True
    content: dict[str, str]
    group: QuestionGroup | None = None

    class Config:
        allow_population_by_field_name = True
        fields = {"round_": "round"}


class QuestionPaginationOut(BaseModel):
    question_ids: list[str]
    cursor: str | None = None


class QuestionGroups(BaseModel):
    groups: list[str]


class QuestionSimpleOut(BaseModel):
    question_id: str
    content: str
    type_: QuestionType | None

    class Config:
        allow_population_by_field_name = True
        fields = {"type_": "type"}
