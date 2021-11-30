from typing import List

from app.question.question_exceptions import QuestionExistsException, QuestionNotFound
from app.question.question_models import NewQuestion, Question
from app.question.question_repository import AbstractQuestionRepository


class FakeQuestionRepository(AbstractQuestionRepository):
    def __init__(self, questions: List[Question]):
        self.questions = questions

    async def add(self, new_question: Question):
        for question in self.questions:
            if question.question_id == new_question.question_id:
                raise QuestionExistsException("question already exists")
        else:
            self.questions.append(new_question)

    async def get(self, question_id: str) -> Question:
        for question in self.questions:
            if question.question_id == question_id:
                return question
        else:
            raise QuestionNotFound("question not found")

    async def remove(self, question_id: str):
        question = await self.get(question_id=question_id)
        self.questions.remove(question)

    async def does_question_exist(self, new_question: NewQuestion) -> bool:
        for question in self.questions:
            if (
                question.round_ == new_question.round_
                and new_question.game_name == question.game_name
                and question.group == new_question.group
                and new_question.language_code in question.content
                and question.content[new_question.language_code] == new_question.content
            ):
                return True
        else:
            return False

    async def update_enable_status(self, question_id: str, enabled: bool) -> Question:
        for question in self.questions:
            if question.question_id == question_id:
                question.enabled = enabled
                return question
        else:
            raise QuestionNotFound("question not found")

    async def add_translation(self, question_id: str, language_code: str, content: str) -> Question:
        question = await self.get(question_id=question_id)
        if language_code in question.content:
            raise QuestionExistsException("language code already ecists for question")
        question.content[language_code] = content
        return question

    async def remove_translation(self, question_id: str, language_code: str):
        question = await self.get(question_id=question_id)
        try:
            del question.content[language_code]
        except KeyError:
            raise QuestionNotFound(f"{language_code=} not found in question {question_id=}")
