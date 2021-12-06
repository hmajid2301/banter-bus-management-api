from typing import Optional

from pydantic import BaseModel

from app.core.models import QuestionGroup


class QuestionTranslationIn(BaseModel):
    content: str


class QuestionTranslationOut(BaseModel):
    question_id: str
    game_name: str
    language_code: str
    round_: Optional[str]
    enabled: bool = True
    content: str
    group: Optional[QuestionGroup] = None

    class Config:
        allow_population_by_field_name = True
        fields = {"round_": "round"}
