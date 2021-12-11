from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.param_functions import Query
from pydantic.error_wrappers import ValidationError
from structlog.stdlib import BoundLogger

from app.core.logger import get_logger
from app.factory import get_read_scopes, get_write_scopes
from app.question.question_api_models import (
    QuestionGroups,
    QuestionIn,
    QuestionOut,
    QuestionPaginationOut,
    QuestionSimpleOut,
)
from app.question.question_exceptions import QuestionExistsException
from app.question.question_factory import get_question_service
from app.question.question_models import Question
from app.question.question_service import AbstractQuestionService
from app.question.translation.question_api import router as translation_router

router = APIRouter(
    prefix="/game/{game_name}/question",
    tags=["questions"],
)
router.include_router(translation_router)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=QuestionOut,
    response_model_exclude_none=True,
    dependencies=[Depends(get_write_scopes)],
)
async def add_question(
    game_name: str,
    question: QuestionIn,
    question_service: AbstractQuestionService = Depends(get_question_service),
    log: BoundLogger = Depends(get_logger),
):
    try:
        log.debug("trying to add new question")
        new_question_dict = {**question.dict(), "game_name": game_name}
        new_question = await question_service.add(question_dict=new_question_dict)
        return new_question.dict()
    except QuestionExistsException as e:
        log.warning("question already exists", question=question.dict())
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error_message": str(e), "error_code": "question_already_exists"},
        )
    except (ValidationError, ValueError) as e:
        log.warning("invalid format", error=e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_message": str(e), "error_code": "question_format_error"},
        )


@router.get(
    ":random",
    status_code=status.HTTP_200_OK,
    response_model=List[QuestionSimpleOut],
)
async def get_random_questions(
    game_name: str,
    round_: str = Query(None, alias="round"),
    language_code: str = "en",
    group_name: Optional[str] = None,
    limit: int = Query(5, ge=1, le=100),
    question_service: AbstractQuestionService = Depends(get_question_service),
    log: BoundLogger = Depends(get_logger),
):
    log.debug("trying to get random questions")
    random_questions = await question_service.get_random(
        game_name=game_name, round_=round_, language_code=language_code, group_name=group_name, limit=limit
    )
    return random_questions


@router.get(
    "/id",
    status_code=status.HTTP_200_OK,
    response_model=QuestionPaginationOut,
    response_model_exclude_none=True,
    dependencies=[Depends(get_read_scopes)],
)
async def get_question_ids(
    game_name: str,
    cursor: Optional[str],
    limit: int = Query(5, ge=1, le=100),
    question_service: AbstractQuestionService = Depends(get_question_service),
    log: BoundLogger = Depends(get_logger),
):
    log.debug("trying to get question ids")
    question_ids = await question_service.get_ids(
        game_name=game_name,
        cursor=cursor,
        limit=limit,
    )
    return question_ids


@router.get(
    "/group:random",
    status_code=status.HTTP_200_OK,
    response_model=QuestionGroups,
)
async def get_random_groups(
    game_name: str,
    round_: str = Query(None, alias="round"),
    limit: int = Query(5, ge=1, le=100),
    question_service: AbstractQuestionService = Depends(get_question_service),
    log: BoundLogger = Depends(get_logger),
):
    try:
        log.debug("trying to get question groups")
        question_groups = await question_service.get_random_groups(game_name=game_name, round_=round_, limit=limit)
        return QuestionGroups(groups=question_groups)
    except ValueError as e:
        log.warning("invalid format", error=e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_message": str(e), "error_code": "format_error"},
        )


@router.get(
    "/{question_id}",
    status_code=status.HTTP_200_OK,
    response_model=QuestionOut,
    response_model_exclude_none=True,
    dependencies=[Depends(get_read_scopes)],
)
async def get_question(
    game_name: str,
    question_id: str,
    question_service: AbstractQuestionService = Depends(get_question_service),
    log: BoundLogger = Depends(get_logger),
):
    log.debug("trying to get a question")
    question = await question_service.get(question_id=question_id, game_name=game_name)
    return question


@router.delete(
    "/{question_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_write_scopes)],
)
async def remove_question(
    game_name: str,
    question_id: str,
    question_service: AbstractQuestionService = Depends(get_question_service),
    log: BoundLogger = Depends(get_logger),
):
    log.debug("trying to remove a question")
    await question_service.remove(question_id=question_id, game_name=game_name)


@router.put(
    "/{question_id}:enable",
    status_code=status.HTTP_200_OK,
    response_model=QuestionOut,
    response_model_exclude_none=True,
    dependencies=[Depends(get_write_scopes)],
)
async def enable_question(
    game_name: str,
    question_id: str,
    question_service: AbstractQuestionService = Depends(get_question_service),
    log: BoundLogger = Depends(get_logger),
):
    question = await _update_enable_status(
        game_name=game_name, question_id=question_id, question_service=question_service, log=log, enabled=True
    )
    return question


@router.put(
    "/{question_id}:disable",
    status_code=status.HTTP_200_OK,
    response_model=QuestionOut,
    response_model_exclude_none=True,
    dependencies=[Depends(get_write_scopes)],
)
async def disable_question(
    game_name: str,
    question_id: str,
    question_service: AbstractQuestionService = Depends(get_question_service),
    log: BoundLogger = Depends(get_logger),
):
    question = await _update_enable_status(
        game_name=game_name, question_id=question_id, question_service=question_service, log=log, enabled=False
    )
    return question


async def _update_enable_status(
    game_name: str, question_id: str, question_service: AbstractQuestionService, log: BoundLogger, enabled: bool
) -> Question:
    log = log.bind(question_id=question_id, new_status=enabled)
    log.debug("trying to update enable status")
    question = await question_service.update_enabled_status(
        game_name=game_name, question_id=question_id, enabled=enabled
    )
    return question
