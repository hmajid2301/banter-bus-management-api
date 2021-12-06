from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.param_functions import Query
from pydantic.error_wrappers import ValidationError
from structlog.stdlib import BoundLogger

from app.factory import get_logger
from app.game.game_exceptions import GameNotFound
from app.question.question_api_models import (
    QuestionGroups,
    QuestionIn,
    QuestionOut,
    QuestionPaginationOut,
    QuestionSimpleOut,
    QuestionTranslationIn,
    QuestionTranslationOut,
)
from app.question.question_exceptions import (
    InvalidLanguageCode,
    InvalidLimit,
    QuestionExistsException,
    QuestionNotFound,
)
from app.question.question_factory import get_question_service
from app.question.question_models import Question
from app.question.question_service import AbstractQuestionService

router = APIRouter(
    prefix="/game/{game_name}/question",
    tags=["questions"],
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=QuestionOut, response_model_exclude_none=True)
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
    except GameNotFound as e:
        log.warning("game not found", game_name=game_name)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "game_not_found"},
        )
    except QuestionExistsException as e:
        log.warning("question already exists", question=question.dict())
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error_message": str(e), "error_code": "question_already_exists"},
        )
    except (ValidationError, ValueError, InvalidLanguageCode) as e:
        log.warning("invalid format", error=e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_message": str(e), "error_code": "question_format_error"},
        )
    except Exception:
        log.exception("failed to add new question")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_message": f"failed to add question {question=}", "error_code": "failed_create_question"},
        )


@router.get(
    "/id",
    status_code=status.HTTP_200_OK,
    response_model=QuestionPaginationOut,
    response_model_exclude_none=True,
)
async def get_question_ids(
    game_name: str,
    cursor: Optional[str],
    limit: int = Query(5, ge=1, le=100),
    question_service: AbstractQuestionService = Depends(get_question_service),
    log: BoundLogger = Depends(get_logger),
):
    try:
        log.debug("trying to get question ids")
        question_ids = await question_service.get_ids(
            game_name=game_name,
            cursor=cursor,
            limit=limit,
        )
        return question_ids
    except GameNotFound as e:
        log.warning("game not found", game_name=game_name)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "game_not_found"},
        )
    except InvalidLimit as e:
        log.warning("invalid limit", error=e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_message": str(e), "error_code": "query_format_error"},
        )
    except Exception:
        log.exception("failed to get question ids")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_message": "failed to get question ids",
                "error_code": "failed_get_question_ids",
            },
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
    try:
        log.debug("trying to get random questions")
        random_questions = await question_service.get_random(
            game_name=game_name, round_=round_, language_code=language_code, group_name=group_name, limit=limit
        )
        return random_questions
    except GameNotFound as e:
        log.warning("game not found", game_name=game_name)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "game_not_found"},
        )
    except InvalidLimit as e:
        log.warning("invalid limit", error=e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_message": str(e), "error_code": "query_format_error"},
        )
    except Exception:
        log.exception("failed to get random questions")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_message": "failed to get random questions",
                "error_code": "failed_get_random_question",
            },
        )


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
    except GameNotFound as e:
        log.warning("game not found", game_name=game_name)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "game_not_found"},
        )
    except ValueError as e:
        log.warning("invalid format", error=e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_message": str(e), "error_code": "format_error"},
        )
    except InvalidLimit as e:
        log.warning("invalid limit", error=e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_message": str(e), "error_code": "query_format_error"},
        )
    except Exception:
        log.exception("failed to get question groups")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_message": "failed to get question groups",
                "error_code": "failed_get_question_groups",
            },
        )


@router.get(
    "/{question_id}", status_code=status.HTTP_200_OK, response_model=QuestionOut, response_model_exclude_none=True
)
async def get_question(
    game_name: str,
    question_id: str,
    question_service: AbstractQuestionService = Depends(get_question_service),
    log: BoundLogger = Depends(get_logger),
):
    try:
        log.debug("trying to get a question")
        question = await question_service.get(question_id=question_id, game_name=game_name)
        return question
    except QuestionNotFound as e:
        log.warning("question not found", question_id=question_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "question_not_found"},
        )
    except GameNotFound as e:
        log.warning("game not found", game_name=game_name)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "game_not_found"},
        )
    except Exception:
        log.exception("failed to get a question")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_message": f"failed to get question {question_id=}", "error_code": "failed_get_question"},
        )


@router.delete("/{question_id}", status_code=status.HTTP_200_OK)
async def remove_question(
    game_name: str,
    question_id: str,
    question_service: AbstractQuestionService = Depends(get_question_service),
    log: BoundLogger = Depends(get_logger),
):
    try:
        log.debug("trying to remove a question")
        await question_service.remove(question_id=question_id, game_name=game_name)
    except QuestionNotFound as e:
        log.warning("question not found", question_id=question_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "question_not_found"},
        )
    except GameNotFound as e:
        log.warning("game not found", game_name=game_name)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "game_not_found"},
        )
    except Exception:
        log.exception("failed to remove a question")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_message": f"failed to remove question {question_id=}",
                "error_code": "failed_remove_question",
            },
        )


@router.put(
    "/{question_id}:enable",
    status_code=status.HTTP_200_OK,
    response_model=QuestionOut,
    response_model_exclude_none=True,
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
    try:
        log = log.bind(question_id=question_id, new_status=enabled)
        log.debug("trying to update enable status")
        question = await question_service.update_enabled_status(
            game_name=game_name, question_id=question_id, enabled=enabled
        )
        return question
    except GameNotFound:
        log.warning("game not found", game_name=game_name)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": f"game {game_name=} does not exist", "error_code": "game_not_found"},
        )
    except QuestionNotFound as e:
        log.warning("question not found", question_id=question_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "question_not_found"},
        )
    except Exception:
        log.exception("failed to update game enabled status")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_message": f"failed to update game {question_id=} enabled status to {enabled=}",
                "error_code": "failed_update_question_enable",
            },
        )


@router.post(
    "/{question_id}/{language_code}",
    status_code=status.HTTP_201_CREATED,
    response_model=QuestionOut,
    response_model_exclude_none=True,
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
    except QuestionNotFound as e:
        log.warning("question not found", question_id=question_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "question_not_found"},
        )
    except GameNotFound as e:
        log.warning("game not found", game_name=game_name)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "game_not_found"},
        )
    except QuestionExistsException as e:
        log.warning("question already exists", language_code=language_code, question=question_translation.dict())
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error_message": str(e), "error_code": "question_already_exists"},
        )
    except InvalidLanguageCode as e:
        log.warning("invalid language code", language_code=language_code)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_message": str(e), "error_code": "question_format_error"},
        )
    except Exception:
        log.exception("failed to add a question translation")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_message": f"failed to add question {question_id=} {language_code=}",
                "error_code": "failed_add_question_translation",
            },
        )


@router.get(
    "/{question_id}/{language_code}",
    status_code=status.HTTP_200_OK,
    response_model=QuestionTranslationOut,
    response_model_exclude_none=True,
)
async def get_question_translation(
    game_name: str,
    question_id: str,
    language_code: str,
    question_service: AbstractQuestionService = Depends(get_question_service),
    log: BoundLogger = Depends(get_logger),
):
    try:
        log.debug("trying to get a question translation")
        question = await question_service.get_translation(
            question_id=question_id, game_name=game_name, language_code=language_code
        )
        return question
    except QuestionNotFound as e:
        log.warning("question not found", question_id=question_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "question_not_found"},
        )
    except GameNotFound as e:
        log.warning("game not found", game_name=game_name)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "game_not_found"},
        )
    except InvalidLanguageCode as e:
        log.warning("invalid language code", language_code=language_code)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_message": str(e), "error_code": "question_format_error"},
        )
    except Exception:
        log.exception("failed to get a question translation")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_message": f"failed to get question {question_id=} {language_code=}",
                "error_code": "failed_get_question_translation",
            },
        )


@router.delete(
    "/{question_id}/{language_code}",
    status_code=status.HTTP_200_OK,
)
async def remove_question_translation(
    game_name: str,
    question_id: str,
    language_code: str,
    question_service: AbstractQuestionService = Depends(get_question_service),
    log: BoundLogger = Depends(get_logger),
):
    try:
        log.debug("trying to remove a question translation")
        question = await question_service.remove_translation(
            question_id=question_id, game_name=game_name, language_code=language_code
        )
        return question
    except QuestionNotFound as e:
        log.warning("question not found", question_id=question_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "question_not_found"},
        )
    except GameNotFound as e:
        log.warning("game not found", game_name=game_name)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "game_not_found"},
        )
    except InvalidLanguageCode as e:
        log.warning("invalid language code", language_code=language_code)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_message": str(e), "error_code": "question_format_error"},
        )
    except Exception:
        log.exception("failed to remove a question translation")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_message": f"failed to get question {question_id=} {language_code=}",
                "error_code": "failed_remove_question_translation",
            },
        )