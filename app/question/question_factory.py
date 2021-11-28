from fastapi import Depends

from app.game.game_factory import get_game_service
from app.game.game_service import AbstractGameService
from app.question.question_repository import (
    AbstractQuestionRepository,
    QuestionRepository,
)
from app.question.question_service import AbstractQuestionService, QuestionService


def get_question_repository() -> AbstractQuestionRepository:
    return QuestionRepository()


def get_question_service(
    question_repository: AbstractQuestionRepository = Depends(get_question_repository),
    game_service: AbstractGameService = Depends(get_game_service),
) -> AbstractQuestionService:
    question_service = QuestionService(question_repository=question_repository, game_service=game_service)
    return question_service
