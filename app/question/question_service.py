import abc
import uuid

import languagecodes
from pymongo.errors import DuplicateKeyError

from app.game.games.game import get_game
from app.question.question_exceptions import (
    InvalidLanguageCode,
    QuestionExistsException,
    QuestionNotFound,
)
from app.question.question_models import NewQuestion, Question, QuestionTranslation
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

    @abc.abstractmethod
    async def update_enabled_status(self, game_name: str, question_id: str, enabled: bool) -> Question:
        raise NotImplementedError

    @abc.abstractmethod
    async def add_translation(self, game_name: str, question_id: str, language_code: str, content: str) -> Question:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_translation(self, game_name: str, question_id: str, language_code: str) -> QuestionTranslation:
        raise NotImplementedError

    @abc.abstractmethod
    async def remove_translation(self, game_name: str, question_id: str, language_code: str) -> QuestionTranslation:
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

            new_question_dict = {**question_dict, "content": {question.language_code: question.content}}
            new_question = Question(**new_question_dict, question_id=id_)

            await self.question_repository.add(new_question)
            return new_question
        except DuplicateKeyError:
            raise QuestionExistsException(f"question {id_=} already exists")

    def _validate_question(self, question: NewQuestion):
        game_name = question.game_name
        game = get_game(game_name=game_name)
        self._validate_language_code(language_code=question.language_code)
        game.validate_question(round_=question.round_ or "", group=question.group)

    async def remove(self, question_id: str, game_name: str):
        get_game(game_name=game_name)
        await self.question_repository.remove(question_id)

    async def get(self, question_id: str, game_name: str) -> Question:
        get_game(game_name=game_name)
        question = await self.question_repository.get(question_id)
        return question

    async def update_enabled_status(self, game_name: str, question_id: str, enabled: bool) -> Question:
        get_game(game_name=game_name)
        question = await self.question_repository.update_enable_status(question_id=question_id, enabled=enabled)
        return question

    async def add_translation(self, game_name: str, question_id: str, language_code: str, content: str) -> Question:
        get_game(game_name=game_name)
        self._validate_language_code(language_code=language_code)
        question = await self.question_repository.add_translation(
            question_id=question_id, language_code=language_code, content=content
        )
        return question

    async def get_translation(self, game_name: str, question_id: str, language_code: str) -> QuestionTranslation:
        get_game(game_name=game_name)
        self._validate_language_code(language_code=language_code)
        question = await self.question_repository.get(question_id)

        try:
            content = question.content[language_code]
            question_dict = question.dict()
            question_dict["content"] = content
            single_content_question = QuestionTranslation(**question_dict, language_code=language_code)
        except KeyError:
            raise QuestionNotFound(f"{language_code} does not exist for question {question_id}")

        return single_content_question

    async def remove_translation(self, game_name: str, question_id: str, language_code: str):
        get_game(game_name=game_name)
        self._validate_language_code(language_code=language_code)
        await self.question_repository.remove_translation(question_id=question_id, language_code=language_code)

    @staticmethod
    def _validate_language_code(language_code: str):
        lang = languagecodes.iso_639_alpha2(language_code)
        if lang is None:
            raise InvalidLanguageCode(f"invalid {language_code=}")
