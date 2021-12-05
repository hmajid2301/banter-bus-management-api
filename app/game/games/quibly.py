from typing import Any, List, Optional

from app.core.models import QuestionGroup
from app.game.games.abstract_game import AbstractGame
from app.story.story_models import QuiblyAnswer


class QuiblyGame(AbstractGame):
    valid_rounds = {"pair", "group", "answer"}

    def validate_question(self, round_: str, group: Optional[QuestionGroup] = None):
        if round_ not in self.valid_rounds:
            raise ValueError(f"expected round to be one of {', '.join(self.valid_rounds)} but received {round_}")

    def has_groups(self, round_: str) -> bool:
        if round_ not in self.valid_rounds:
            raise ValueError(f"expected round to be one of {', '.join(self.valid_rounds)} but received {round_}")

        return False

    def get_question_type(self, round_: str, group: Optional[QuestionGroup] = None) -> str:
        type_ = "question"
        if round_ == "answer":
            type_ = "answer"

        return type_

    def validate_story(self, nickname: str, round_: str, answers: List[Any]):
        if nickname:
            raise ValueError("unexpected field `nickname` for quibly")

        if round_ not in self.valid_rounds:
            raise ValueError(f"expected round to be one of {', '.join(self.valid_rounds)} but received {round_}")

        for answer in answers:
            if not isinstance(answer, QuiblyAnswer):
                raise ValueError("answers field doesn't match expected format")
