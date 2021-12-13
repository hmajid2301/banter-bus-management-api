import random
import uuid
from typing import List, Optional

import languagecodes

from app.game.games.game import get_game
from app.question.question_exceptions import (
    InvalidLanguageCode,
    InvalidLimit,
    QuestionExistsException,
    QuestionNotFound,
)
from app.question.question_models import (
    NewQuestion,
    Question,
    QuestionIDsPagination,
    QuestionSimple,
    QuestionTranslation,
)
from app.question.question_repository import AbstractQuestionRepository


class QuestionService:
    def __init__(self, question_repository: AbstractQuestionRepository):
        self.question_repository = question_repository

    async def add(self, question_dict: dict) -> Question:
        id_ = str(uuid.uuid4())
        question = NewQuestion(**question_dict)

        self._validate_question(question=question)
        exists = await self.question_repository.does_question_exist(new_question=question)
        if exists:
            raise QuestionExistsException(f"question {question_dict} already exists")

        new_question_dict = {**question_dict, "content": {question.language_code: question.content}}
        new_question = Question(**new_question_dict, question_id=id_)

        await self.question_repository.add(new_question)
        return new_question

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
            raise QuestionNotFound(question_id=question_id, language_code=language_code)

        return single_content_question

    async def remove_translation(self, game_name: str, question_id: str, language_code: str):
        get_game(game_name=game_name)
        self._validate_language_code(language_code=language_code)
        await self.question_repository.remove_translation(question_id=question_id, language_code=language_code)

    async def get_ids(self, game_name: str, limit: int, cursor: Optional[str] = None) -> QuestionIDsPagination:
        get_game(game_name=game_name)
        if limit < 1:
            raise InvalidLimit(limit=limit, min=0)

        question_ids = await self.question_repository.get_ids(game_name=game_name, limit=limit, cursor=cursor)
        new_cursor = None
        if len(question_ids) == limit:
            new_cursor = question_ids[-1]

        question_pagination = QuestionIDsPagination(question_ids=question_ids, cursor=new_cursor)
        return question_pagination

    async def get_random(
        self, game_name: str, round_: str, language_code: str, limit: int, group_name: Optional[str] = None
    ) -> List[QuestionSimple]:
        game = get_game(game_name=game_name)
        if limit < 1:
            raise InvalidLimit(limit=limit, min=0)

        if group_name:
            questions = await self.question_repository.get_questions_in_group(
                game_name=game_name, round_=round_, language_code=language_code, group_name=group_name
            )
        else:
            questions = await self.question_repository.get_random(
                game_name=game_name, round_=round_, language_code=language_code, limit=limit
            )
        questions_simple: List[QuestionSimple] = []
        for question in questions:
            question_type = game.get_question_type(round_, group=question.group)
            questions_simple.append(
                QuestionSimple(
                    question_id=question.question_id, content=question.content[language_code], type_=question_type
                )
            )

        return questions_simple

    async def get_random_groups(self, game_name: str, round_: str, limit: int = 1) -> List[str]:
        game = get_game(game_name=game_name)
        game_round_has_groups = game.has_groups(round_=round_)

        if limit < 0:
            raise InvalidLimit(limit=limit, min=0)

        random_groups: List[str] = []
        if game_round_has_groups:
            groups = await self.question_repository.get_groups(game_name=game_name, round_=round_)

            num_of_items = min(len(groups), limit)
            random_groups = random.sample(groups, k=num_of_items)

        return random_groups

    @staticmethod
    def _validate_language_code(language_code: str):
        lang = languagecodes.iso_639_alpha2(language_code)
        if lang is None:
            raise InvalidLanguageCode(language_code=language_code)
