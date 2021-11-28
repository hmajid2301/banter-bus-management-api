import abc
import uuid

from pymongo.errors import DuplicateKeyError

from app.game.games.game import get_game
from app.question.question_exceptions import QuestionExistsException
from app.question.question_models import NewQuestion, Question
from app.question.question_repository import AbstractQuestionRepository


class AbstractQuestionService(abc.ABC):
    @abc.abstractmethod
    async def add(self, question_dict: dict) -> Question:
        raise NotImplementedError

    @abc.abstractmethod
    async def remove(self, question_id: str, game_name: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, question_id: str, game_name: str) -> Question:
        raise NotImplementedError


class QuestionService(AbstractQuestionService):
    def __init__(self, question_repository: AbstractQuestionRepository):
        self.question_repository = question_repository

    async def add(self, question_dict: dict) -> Question:
        id_ = str(uuid.uuid4())
        question = NewQuestion(**question_dict)
        try:
            self._validate_question(question=question)
            exists = await self.question_repository.does_question_exist(new_question=question)
            if exists:
                raise QuestionExistsException(f"question {question_dict} already exists")

            new_question_dict = {**question_dict, "content": {question.language: question.content}}
            new_question = Question(**new_question_dict, id=id_)

            await self.question_repository.add(new_question)
            return new_question
        except DuplicateKeyError:
            raise QuestionExistsException(f"question {id_=} already exists")

    def _validate_question(self, question: NewQuestion):
        game_name = question.game_name
        game = get_game(game_name=game_name)
        game.validate_language_code(language_code=question.language)
        game.validate_question(round_=question.round_ or "", group=question.group)

    async def remove(self, question_id: str, game_name: str):
        get_game(game_name=game_name)
        await self.question_repository.remove(question_id)

    async def get(self, question_id: str, game_name: str) -> Question:
        get_game(game_name=game_name)
        question = await self.question_repository.get(question_id)
        return question
