from enum import Enum
from typing import Dict, List, Optional

from beanie import Document, Indexed
from pydantic import BaseModel

from app.core.models import QuestionGroup


class QuestionIDsPagination(BaseModel):
    question_ids: List[str]
    cursor: Optional[str] = None


class Question(Document):
    question_id: Indexed(str, unique=True)  # type: ignore
    game_name: str
    round_: Optional[str]
    enabled: bool = True
    content: Dict[str, str]
    group: Optional[QuestionGroup] = None

    class Config:
        allow_population_by_field_name = True
        fields = {"round_": "round"}


class QuestionTranslation(BaseModel):
    question_id: str
    game_name: str
    round_: Optional[str]
    language_code: str
    enabled: bool = True
    content: str
    group: Optional[QuestionGroup] = None

    class Config:
        allow_population_by_field_name = True
        fields = {"round_": "round"}


class NewQuestion(BaseModel):
    game_name: str
    round_: Optional[str]
    content: str
    language_code: str = "en"
    group: Optional[QuestionGroup] = None

    class Config:
        allow_population_by_field_name = True
        fields = {"round_": "round"}


class QuestionType(str, Enum):
    answer = "answer"
    question = "question"


class QuestionSimple(BaseModel):
    question_id: str
    content: str
    type_: QuestionType

    class Config:
        allow_population_by_field_name = True
        fields = {"type_": "type"}


class QuestionGroups(BaseModel):
    groups: List[str]
