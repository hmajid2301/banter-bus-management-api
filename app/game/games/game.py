import abc
from typing import Any, Dict, List

import languagecodes

from app.core.models import CaertsianCoordinateColor, QuestionGroup
from app.game.game_exceptions import GameNotFound
from app.story.story_models import FibbingItAnswer, QuiblyAnswer


class AbstractGame(abc.ABC):
    @staticmethod
    def validate_language_code(language_code: str):
        lang = languagecodes.iso_639_alpha3("en")
        if lang is None:
            raise ValueError(f"invalid {language_code=}")

    @abc.abstractmethod
    def validate_question(self, round_: str, group: QuestionGroup = None):
        raise NotImplementedError

    @abc.abstractmethod
    def validate_story(self, nickname: str, round_: str, answers: List[Any]):
        raise NotImplementedError


class FibbingItGame(AbstractGame):
    valid_rounds = {"opinion", "likely", "free_form"}

    def validate_question(self, round_: str, group: QuestionGroup = None):
        allowed_types = {"answer", "question"}
        rounds_with_groups = {"free_form", "opinion"}
        rounds_with_group_types = {"opinion"}

        if round_ not in self.valid_rounds:
            raise ValueError(f"expected round to be one of {', '.join(self.valid_rounds)} but received {round_}")

        if not group and round_ in rounds_with_groups:
            raise ValueError("`group` field must be set on fibbing_it games")

        if group and (group.name is None):
            raise ValueError("`group.name` field must be set on fibbing_it games")

        if group and (group.type_ not in allowed_types) and (round_ in rounds_with_group_types):
            raise ValueError(
                f"`group.type` field expected to be one of {', '.join(allowed_types)} but received {group.type_}"
            )

    def validate_story(self, nickname: str, round_: str, answers: List[Any]):

        if nickname:
            raise ValueError("unexpected field `nickname` for fibbing_it")

        if round_ not in self.valid_rounds:
            raise ValueError(f"expected round to be one of {', '.join(self.valid_rounds)} but received {round_}")

        for answer in answers:
            if not isinstance(answer, FibbingItAnswer):
                raise ValueError("answers field doesn't match expected format")


class QuiblyGame(AbstractGame):
    valid_rounds = {"pair", "group", "answer"}

    def validate_question(self, round_: str, group: QuestionGroup = None):
        if round_ not in self.valid_rounds:
            raise ValueError(f"expected round to be one of {', '.join(self.valid_rounds)} but received {round_}")

    def validate_story(self, nickname: str, round_: str, answers: List[Any]):
        if nickname:
            raise ValueError("unexpected field `nickname` for quibly")

        if round_ not in self.valid_rounds:
            raise ValueError(f"expected round to be one of {', '.join(self.valid_rounds)} but received {round_}")

        for answer in answers:
            if not isinstance(answer, QuiblyAnswer):
                raise ValueError("answers field doesn't match expected format")


class DrawlosseumGame(AbstractGame):
    def validate_question(self, round_: str, group: QuestionGroup = None):
        pass

    def validate_story(self, nickname: str, round_: str, answers: List[Any]):
        if not nickname:
            raise ValueError("nickname is a required field for drawlosseum")

        if round_:
            raise ValueError("unexpected field `round` for drawlosseum")

        for answer in answers:
            if not isinstance(answer, CaertsianCoordinateColor):
                raise ValueError("answers field doesn't match expected format")


def get_game(game_name: str) -> AbstractGame:
    valid_games: Dict[str, AbstractGame] = {
        "quibly": QuiblyGame(),
        "fibbing_it": FibbingItGame(),
        "drawlosseum": DrawlosseumGame(),
    }

    try:
        game = valid_games[game_name]
    except KeyError:
        raise GameNotFound(f"game {game_name=} not found")

    return game
