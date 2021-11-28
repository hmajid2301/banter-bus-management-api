import abc
from typing import List

from app.core.repository import AbstractRepository
from app.question.question_exceptions import QuestionNotFound
from app.question.question_models import NewQuestion, Question


class AbstractQuestionRepository(AbstractRepository[Question]):
    @abc.abstractmethod
    async def does_question_exist(self, new_question: NewQuestion) -> bool:
        raise NotImplementedError


class QuestionRepository(AbstractQuestionRepository):
    async def add(self, question: Question):
        await Question.insert(question)

    async def get(self, question_id: str) -> Question:
        question = await Question.find_one(Question.id == question_id)
        if not question:
            raise QuestionNotFound(f"unable to find {question_id=}")

        return question

    async def remove(self, question_id: str):
        await self.get(question_id=question_id)
        await Question.find_one(Question.id == question_id).delete()

    async def does_question_exist(self, new_question: NewQuestion) -> bool:
        questions: List[Question] = await Question.find(
            Question.round_ == new_question.round_,
            Question.game_name == new_question.game_name,
            Question.group == new_question.group,
        ).to_list()

        for question in questions:
            try:
                content = question.content[new_question.language]
                if content == new_question.content:
                    return True
            except KeyError:
                continue

        else:
            return False
