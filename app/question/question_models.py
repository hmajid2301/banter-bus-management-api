import abc
from typing import Dict, Optional

import languagecodes
from beanie import Document
from pydantic import BaseModel, root_validator

from app.core.models import QuestionGroup
from app.game.game_exceptions import GameNotFound


class Question(Document):
    id: str
    game_name: str
    round_: Optional[str]
    enabled: bool = True
    content: Dict[str, str]
    group: Optional[QuestionGroup] = None

    class Config:
        allow_population_by_field_name = True
        fields = {"id_": "id", "round_": "round"}


class NewQuestion(BaseModel):
    game_name: str
    round_: Optional[str]
    content: str
    language: str = "en"
    group: Optional[QuestionGroup] = None

    class Config:
        allow_population_by_field_name = True
        fields = {"round_": "round"}

    @root_validator()
    def validate(cls, values: dict):
        try:
            language = values["language"]
        except KeyError:
            raise ValueError("expected `language` to be a field in NewQuestion")

        validate_game_story_map: Dict[str, AbstractQuestionValidator] = {
            "quibly": QuiblyValidator(language_code=language),
            "fibbing_it": FibbingItValidator(language_code=language),
            "drawlosseum": DrawlosseumValidator(language_code=language),
        }

        try:
            game_name = values["game_name"]
        except KeyError:
            raise ValueError("expected `game_name` to be a field in NewQuestion")

        try:
            game = validate_game_story_map[game_name]
            round_, group = values["round_"], values["group"]
            game.validate_question(round_=round_, group=group)
        except KeyError:
            raise GameNotFound(f"invalid {game_name=}")

        return values


class AbstractQuestionValidator(abc.ABC):
    def __init__(self, language_code: str):
        self.validate_language_code(language_code=language_code)

    @staticmethod
    def validate_language_code(language_code: str):
        lang = languagecodes.iso_639_alpha3("en")
        if lang is None:
            raise ValueError(f"invalid {language_code=}")

    @abc.abstractmethod
    def validate_question(self, round_: str, group: QuestionGroup = None):
        raise NotImplementedError


class FibbingItValidator(AbstractQuestionValidator):
    def validate_question(self, round_: str, group: QuestionGroup = None):
        valid_rounds = {"opinion", "likely", "free_form"}
        allowed_types = {"answer", "question"}
        rounds_with_groups = {"free_form", "opinion"}
        rounds_with_group_types = {"opinion"}

        if round_ not in valid_rounds:
            raise ValueError(f"expected round to be one of {', '.join(valid_rounds)} but received {round_}")

        if not group and round_ in rounds_with_groups:
            raise ValueError("`group` field must be set on fibbing_it games")

        if group and (group.name is None):
            raise ValueError("`group.name` field must be set on fibbing_it games")

        if group and (group.type_ not in allowed_types) and (round_ in rounds_with_group_types):
            raise ValueError(
                f"`group.type` field expected to be one of {', '.join(allowed_types)} but received {group.type_}"
            )


class QuiblyValidator(AbstractQuestionValidator):
    def validate_question(self, round_: str, group: QuestionGroup = None):
        valid_rounds = {"pair", "group", "answer"}

        if round_ not in valid_rounds:
            raise ValueError(f"expected round to be one of {', '.join(valid_rounds)} but received {round_}")


class DrawlosseumValidator(AbstractQuestionValidator):
    def validate_question(self, round_: str, group: QuestionGroup = None):
        pass
