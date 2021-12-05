import abc
from typing import Any, List, Optional

from app.core.models import QuestionGroup


class AbstractGame(abc.ABC):
    @abc.abstractmethod
    def validate_question(self, round_: str, group: Optional[QuestionGroup] = None):
        raise NotImplementedError

    @abc.abstractmethod
    def has_groups(self, round_: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get_question_type(self, round_: str, group: Optional[QuestionGroup] = None) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def validate_story(self, nickname: str, round_: str, answers: List[Any]):
        raise NotImplementedError
