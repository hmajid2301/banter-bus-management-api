import abc
from typing import List

from app.core.repository import AbstractRepository
from app.question.question_exceptions import QuestionExistsException, QuestionNotFound
from app.question.question_models import NewQuestion, Question


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


class QuestionRepository(AbstractQuestionRepository):
    async def add(self, question: Question):
        await Question.insert(question)

    async def get(self, question_id: str) -> Question:
        question = await Question.find_one(Question.question_id == question_id)
        if not question:
            raise QuestionNotFound(f"unable to find {question_id=}")

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
            raise QuestionNotFound(f"{language_code=} not found in question {question_id=}")
        await question.save()
