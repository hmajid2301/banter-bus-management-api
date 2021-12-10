from fastapi import APIRouter, Depends, HTTPException, status
from structlog.stdlib import BoundLogger

from app.factory import get_logger, get_read_scopes, get_write_scopes
from app.game.game_exceptions import GameNotFound
from app.question.question_api_models import QuestionOut
from app.question.question_exceptions import (
    InvalidLanguageCode,
    QuestionExistsException,
    QuestionNotFound,
)
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
