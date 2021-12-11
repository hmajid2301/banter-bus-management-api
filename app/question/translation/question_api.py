from fastapi import APIRouter, Depends, HTTPException, status
from structlog.stdlib import BoundLogger

from app.core.logger import get_logger
from app.factory import get_read_scopes, get_write_scopes
from app.question.question_api_models import QuestionOut
from app.question.question_exceptions import QuestionExistsException
from app.question.question_factory import get_question_service
from app.question.question_service import AbstractQuestionService
from app.question.translation.question_translation_api_models import (
    QuestionTranslationIn,
    QuestionTranslationOut,
)

router = APIRouter(
    prefix="/{question_id}/{language_code}",
    tags=["questions"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=QuestionOut,
    response_model_exclude_none=True,
    dependencies=[Depends(get_write_scopes)],
)
async def add_question_translation(
    game_name: str,
    question_id: str,
    language_code: str,
    question_translation: QuestionTranslationIn,
    question_service: AbstractQuestionService = Depends(get_question_service),
    log: BoundLogger = Depends(get_logger),
):
    try:
        log.debug("trying to add a question translation")
        content = question_translation.content
        question = await question_service.add_translation(
            question_id=question_id, game_name=game_name, language_code=language_code, content=content
        )
        return question
    except QuestionExistsException as e:
        log.warning("question already exists", language_code=language_code, question=question_translation.dict())
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error_message": str(e), "error_code": "question_already_exists"},
        )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=QuestionTranslationOut,
    response_model_exclude_none=True,
    dependencies=[Depends(get_read_scopes)],
)
async def get_question_translation(
    game_name: str,
    question_id: str,
    language_code: str,
    question_service: AbstractQuestionService = Depends(get_question_service),
    log: BoundLogger = Depends(get_logger),
):
    log.debug("trying to get a question translation")
    question = await question_service.get_translation(
        question_id=question_id, game_name=game_name, language_code=language_code
    )
    return question


@router.delete(
    "",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_write_scopes)],
)
async def remove_question_translation(
    game_name: str,
    question_id: str,
    language_code: str,
    question_service: AbstractQuestionService = Depends(get_question_service),
    log: BoundLogger = Depends(get_logger),
):
    log.debug("trying to remove a question translation")
    question = await question_service.remove_translation(
        question_id=question_id, game_name=game_name, language_code=language_code
    )
    return question
