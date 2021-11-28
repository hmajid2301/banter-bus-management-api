from fastapi import APIRouter, Depends, HTTPException, status
from pydantic.error_wrappers import ValidationError
from structlog.stdlib import BoundLogger

from app.factory import get_logger
from app.game.game_exceptions import GameNotFound
from app.question.question_api_models import QuestionIn, QuestionOut
from app.question.question_exceptions import QuestionExistsException, QuestionNotFound
from app.question.question_factory import get_question_service
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "game_not_found"},
        )
    except QuestionExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error_message": str(e), "error_code": "question_already_exists"},
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_message": str(e), "error_code": "question_format_error"},
        )
    except Exception:
        log.exception("failed to add new question")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_message": f"failed to add question {game_name=}", "error_code": "failed_create_question"},
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "question_not_found"},
        )
    except GameNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "game_not_found"},
        )
    except Exception:
        log.exception("failed to get a question")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_message": f"failed to get question {game_name=}", "error_code": "failed_get_question"},
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "question_not_found"},
        )
    except GameNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "game_not_found"},
        )
    except Exception:
        log.exception("failed to remove a question")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_message": f"failed to remove question {game_name=}", "error_code": "failed_remove_question"},
        )
