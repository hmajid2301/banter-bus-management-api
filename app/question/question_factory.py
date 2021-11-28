from fastapi import Depends

from app.question.question_repository import (
    AbstractQuestionRepository,
    QuestionRepository,
)
from app.question.question_service import AbstractQuestionService, QuestionService


def get_question_repository() -> AbstractQuestionRepository:
    return QuestionRepository()


def get_question_service(
    question_repository: AbstractQuestionRepository = Depends(get_question_repository),
) -> AbstractQuestionService:
    question_service = QuestionService(question_repository=question_repository)
    return question_service
