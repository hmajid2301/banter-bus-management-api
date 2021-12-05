from typing import Any, List, Optional

from app.core.models import QuestionGroup
from app.game.games.abstract_game import AbstractGame
from app.story.story_models import FibbingItAnswer


class FibbingItGame(AbstractGame):
    valid_rounds = {"opinion", "likely", "free_form"}

    def validate_question(self, round_: str, group: Optional[QuestionGroup] = None):
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

    def has_groups(self, round_: str) -> bool:
        has_groups = False
        if round_ not in self.valid_rounds:
            raise ValueError(f"expected round to be one of {', '.join(self.valid_rounds)} but received {round_}")

        if round_ in {"opinion", "free_form"}:
            has_groups = True

        return has_groups

    def get_question_type(self, round_: str, group: Optional[QuestionGroup] = None) -> str:
        type_ = "question"
        if group and group.type_:
            type_ = group.type_

        return type_

    def validate_story(self, nickname: str, round_: str, answers: List[Any]):
        if nickname:
            raise ValueError("unexpected field `nickname` for fibbing_it")

        if round_ not in self.valid_rounds:
            raise ValueError(f"expected round to be one of {', '.join(self.valid_rounds)} but received {round_}")

        for answer in answers:
            if not isinstance(answer, FibbingItAnswer):
                raise ValueError("answers field doesn't match expected format")
