import abc
from typing import List, Optional

from beanie.operators import GT, Exists
from omnibus.database.repository import AbstractRepository
from pymongo.errors import DuplicateKeyError

from app.question.question_exceptions import QuestionExistsException, QuestionNotFound
from app.question.question_models import NewQuestion, Question, QuestionGroups


class AbstractQuestionRepository(AbstractRepository[Question]):
    @abc.abstractmethod
    async def does_question_exist(self, new_question: NewQuestion) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_enable_status(self, question_id: str, enabled: bool) -> Question:
        raise NotImplementedError

    @abc.abstractmethod
    async def add_translation(self, question_id: str, language_code: str, content: str) -> Question:
        raise NotImplementedError

    @abc.abstractmethod
    async def remove_translation(self, question_id: str, language_code: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_ids(self, game_name: str, limit: int, cursor: Optional[str] = None) -> List[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_random(self, game_name: str, round_: str, language_code: str, limit: int) -> List[Question]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_questions_in_group(
        self, game_name: str, round_: str, language_code: str, group_name: str
    ) -> List[Question]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_groups(self, game_name: str, round_: str) -> List[str]:
        raise NotImplementedError


class QuestionRepository(AbstractQuestionRepository):
    async def add(self, question: Question):
        try:
            await Question.insert(question)
        except DuplicateKeyError:
            raise QuestionExistsException(f"question {question.question_id=} already exists")

    async def get(self, question_id: str) -> Question:
        question = await Question.find_one(Question.question_id == question_id)
        if not question:
            raise QuestionNotFound(question_id=question_id)

        return question

    async def remove(self, question_id: str):
        await self.get(question_id=question_id)
        await Question.find_one(Question.question_id == question_id).delete()

    async def does_question_exist(self, new_question: NewQuestion) -> bool:
        questions: List[Question] = await Question.find(
            Question.round_ == new_question.round_,
            Question.game_name == new_question.game_name,
            Question.group == new_question.group,
        ).to_list()

        for question in questions:
            try:
                content = question.content[new_question.language_code]
                if content == new_question.content:
                    return True
            except KeyError:
                continue

        else:
            return False

    async def update_enable_status(self, question_id: str, enabled: bool) -> Question:
        question = await self.get(question_id=question_id)
        question.enabled = enabled
        await question.save()
        return question

    async def add_translation(self, question_id: str, language_code: str, content: str) -> Question:
        question = await self.get(question_id=question_id)
        if language_code in question.content:
            raise QuestionExistsException(f"question translation {language_code=} already exists for {question_id=}")
        question.content[language_code] = content
        await question.save()
        return question

    async def remove_translation(self, question_id: str, language_code: str):
        question = await self.get(question_id=question_id)
        try:
            del question.content[language_code]
        except KeyError:
            raise QuestionNotFound(question_id=question_id, language_code=language_code)
        await question.save()

    async def get_ids(self, game_name: str, limit: int, cursor: Optional[str] = None) -> List[str]:
        questions = (
            await Question.find(Question.game_name == game_name, GT(Question.question_id, cursor))
            .limit(limit)
            .to_list()
        )
        question_ids = [question.question_id for question in questions]
        return question_ids

    async def get_random(self, game_name: str, round_: str, language_code: str, limit: int) -> List[Question]:
        questions = (
            await Question.find(
                Question.game_name == game_name,
                Question.round_ == round_,
                Exists(Question.content[language_code], True),
            )
            .aggregate(
                [
                    {
                        "$sample": {"size": limit},
                    },
                ],
                projection_model=Question,
            )
            .to_list()
        )

        return questions

    async def get_questions_in_group(
        self, game_name: str, round_: str, language_code: str, group_name: str
    ) -> List[Question]:
        questions = await Question.find(
            Question.game_name == game_name,
            Question.round_ == round_,
            Question.group.name == group_name,  # type: ignore
            Exists(Question.content[language_code], True),
        ).to_list()
        return questions

    async def get_groups(self, game_name: str, round_: str) -> List[str]:
        # TODO: move to when fixed https://github.com/roman-right/beanie/issues/133
        question_groups_list: List[QuestionGroups] = (
            await Question.find(Question.game_name == game_name, Question.round_ == round_)
            .aggregate(
                [
                    {
                        "$group": {
                            "_id": 1,
                            "groups": {"$addToSet": "$group.name"},
                        },
                    },
                ],
                projection_model=QuestionGroups,
            )
            .to_list()
        )

        question_groups = question_groups_list[0]
        return question_groups.groups
