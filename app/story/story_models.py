import abc
from typing import Any, Dict, List, Optional, Union

from beanie import Document
from pydantic import BaseModel, root_validator

from app.core.models import CaertsianCoordinateColor


class FibbingItAnswer(BaseModel):
    nickname: str
    answer: str


class QuiblyAnswer(BaseModel):
    nickname: str
    answer: str
    votes: int


class Story(Document):
    id: str
    game_name: str
    question: str
    round: Optional[str]
    nickname: Optional[str]
    answers: Union[List[QuiblyAnswer], List[FibbingItAnswer], List[CaertsianCoordinateColor]]

    @root_validator()
    def check_expected_fields_set(cls, values):
        validate_game_story_map: Dict[str, AbstractStoryValidator] = {
            "quibly": QuiblyValidator(),
            "fibbing_it": FibbingItValidator(),
            "drawlosseum": DrawlosseumValidator(),
        }

        try:
            game_name = values["game_name"]
        except KeyError:
            raise ValueError("expected `game_name` to be a field in Story")

        try:
            game = validate_game_story_map[game_name]
            nickname, round, answers = values["nickname"], values["round"], values["answers"]
            game.validate_story(nickname=nickname, round=round, answers=answers)
        except KeyError:
            raise ValueError(f"invalid {game_name=}")

        return values


class AbstractStoryValidator(abc.ABC):
    @abc.abstractmethod
    def validate_story(self, nickname: str, round: str, answers: List[Any]):
        raise NotImplementedError


class FibbingItValidator(AbstractStoryValidator):
    def validate_story(self, nickname: str, round: str, answers: List[Any]):
        valid_rounds = {"opinion", "likely", "free_form"}

        if nickname:
            raise ValueError("unexpected field `nickname` for fibbing_it")

        if round not in valid_rounds:
            raise ValueError(f"expected round to be one of {', '.join(valid_rounds)} but received {round}")

        for answer in answers:
            if not isinstance(answer, FibbingItAnswer):
                raise ValueError("answers field doesn't match expected format")


class QuiblyValidator(AbstractStoryValidator):
    def validate_story(self, nickname: str, round: str, answers: List[Any]):
        valid_rounds = {"pair", "group", "answers"}

        if nickname:
            raise ValueError("unexpected field `nickname` for quibly")

        if round not in valid_rounds:
            raise ValueError(f"expected round to be one of {', '.join(valid_rounds)} but received {round}")

        for answer in answers:
            if not isinstance(answer, QuiblyAnswer):
                raise ValueError("answers field doesn't match expected format")


class DrawlosseumValidator(AbstractStoryValidator):
    def validate_story(self, nickname: str, round: str, answers: List[Any]):
        if not nickname:
            raise ValueError("nickname is a required field for drawlosseum")

        if round:
            raise ValueError("unexpected field `round` for drawlosseum")

        for answer in answers:
            if not isinstance(answer, CaertsianCoordinateColor):
                raise ValueError("answers field doesn't match expected format")
