from typing import Dict, Optional

from beanie import Document
from pydantic import BaseModel

from app.core.models import QuestionGroup


class Question(Document):
    question_id: str
    game_name: str
    round_: Optional[str]
    enabled: bool = True
    content: Dict[str, str]
    group: Optional[QuestionGroup] = None

    class Config:
        allow_population_by_field_name = True
        fields = {"round_": "round"}


class NewQuestion(BaseModel):
    game_name: str
    round_: Optional[str]
    content: str
    language: str = "en"
    group: Optional[QuestionGroup] = None

    class Config:
        allow_population_by_field_name = True
        fields = {"round_": "round"}
