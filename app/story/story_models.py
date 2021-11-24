from typing import List, Optional, Union

from beanie import Document
from pydantic import BaseModel, root_validator, validator


class FibbingItAnswer(BaseModel):
    nickname: str
    answer: str


class QuiblyAnswer(BaseModel):
    nickname: str
    answer: str
    votes: int


class DrawingPoint(BaseModel):
    x: float
    y: float


class CaertsianCoordinateColor(BaseModel):
    start: DrawingPoint
    end: DrawingPoint
    color: str


class Story(Document):
    id: str
    game_name: str
    question: str
    round: Optional[str]
    nickname: Optional[str]
    answers: Union[List[QuiblyAnswer], List[FibbingItAnswer], List[CaertsianCoordinateColor]]

    @root_validator()
    def check_expected_fields_set(cls, values):
        game_name_expected_fields_map = {
            "quibly": {"allowed_fields": ["round"], "not_allowed_fields": ["nickname"]},
            "fibbing_it": {"allowed_fields": ["round"], "not_allowed_fields": ["nickname"]},
            "drawlosseum": {"allowed_fields": ["nickname"], "not_allowed_fields": ["round"]},
        }

        game_name = values.get("game_name", "game name not set")
        try:
            optional_fields = game_name_expected_fields_map[game_name]
            allowed_optional_fields = optional_fields["allowed_fields"]
            for field in allowed_optional_fields:
                if values[field] is None:
                    raise ValueError(
                        f"{game_name=} expects following fields to also be set {', '.join(allowed_optional_fields)}"
                    )

            not_allowed_fields = optional_fields["not_allowed_fields"]
            for field in not_allowed_fields:
                if values[field] is not None:
                    raise ValueError(
                        f"{game_name=} expects following fields to not be set {', '.join(not_allowed_fields)}"
                    )
        except KeyError:
            raise ValueError(f"invalid {game_name=}")

        return values

    @validator("answers")
    def answer_type(cls, v, values):
        game_name = values.get("game_name", "game name not set")
        game_name_expected_type_map = {
            "quibly": QuiblyAnswer,
            "fibbing_it": FibbingItAnswer,
            "drawlosseum": CaertsianCoordinateColor,
        }

        try:
            first_answer = v[0]
            expected_answer_type = game_name_expected_type_map[game_name]
            if not isinstance(first_answer, expected_answer_type):
                raise ValueError(f"{game_name=} doesn't match expected `answer` field format")
        except KeyError:
            raise ValueError(f"invalid {game_name=}")

        return v
