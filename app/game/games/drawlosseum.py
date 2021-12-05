from typing import Any, List, Optional

from app.core.models import CaertsianCoordinateColor, QuestionGroup
from app.game.games.abstract_game import AbstractGame


class DrawlosseumGame(AbstractGame):
    valid_rounds = {"drawing"}

    def validate_question(self, round_: str, group: Optional[QuestionGroup] = None):
        if round_ not in self.valid_rounds:
            raise ValueError(f"expected round to be one of {', '.join(self.valid_rounds)} but received {round_}")

    def has_groups(self, round_: str) -> bool:
        if round_ not in self.valid_rounds:
            raise ValueError(f"expected round to be one of {', '.join(self.valid_rounds)} but received {round_}")

        return False

    def get_question_type(self, round_: str, group: Optional[QuestionGroup] = None) -> str:
        return "question"

    def validate_story(self, nickname: str, round_: str, answers: List[Any]):
        if not nickname:
            raise ValueError("nickname is a required field for drawlosseum")

        if round_ not in self.valid_rounds:
            raise ValueError(f"expected round to be one of {', '.join(self.valid_rounds)} but received {round_}")

        for answer in answers:
            if not isinstance(answer, CaertsianCoordinateColor):
                raise ValueError("answers field doesn't match expected format")
