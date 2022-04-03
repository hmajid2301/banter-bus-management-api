from typing import Dict, List, Optional

from pydantic import BaseModel

from app.core.models import QuestionGroup
from app.question.question_models import QuestionType


class QuestionIn(BaseModel):
    round_: Optional[str]
    content: str
    language_code: str = "en"
    group: Optional[QuestionGroup] = None

    class Config:
        allow_population_by_field_name = True
        fields = {"round_": "round"}


class QuestionOut(BaseModel):
    question_id: str
    game_name: str
    round_: Optional[str]
    enabled: bool = True
    content: Dict[str, str]
    group: Optional[QuestionGroup] = None

    class Config:
        allow_population_by_field_name = True
        fields = {"round_": "round"}


class QuestionPaginationOut(BaseModel):
    question_ids: List[str]
    cursor: Optional[str] = None


class QuestionGroups(BaseModel):
    groups: List[str]


class QuestionSimpleOut(BaseModel):
    question_id: str
    content: str
    type_: Optional[QuestionType]

    class Config:
        allow_population_by_field_name = True
        fields = {"type_": "type"}
