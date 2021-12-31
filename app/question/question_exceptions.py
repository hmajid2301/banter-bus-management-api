from typing import Optional

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from omnibus.log.logger import get_logger

from app.core.exceptions import (
    ExistsException,
    IncorrectFormatException,
    NotFoundException,
)


class QuestionNotFound(NotFoundException):
    def __init__(self, question_id: str, language_code: Optional[str] = None) -> None:
        self.question_id = question_id
        self.language_code = language_code


class QuestionExistsException(ExistsException):
    pass


class InvalidLanguageCode(IncorrectFormatException):
    def __init__(self, language_code: str) -> None:
        self.language_code = language_code


class InvalidLimit(IncorrectFormatException):
    def __init__(self, limit: int, min: int, max: Optional[int] = None) -> None:
        self.limit = limit
        self.min = min
        self.max = max


def add_question_exceptions(app: FastAPI):
    @app.exception_handler(QuestionNotFound)
    async def question_not_found_exception_handler(request: Request, exc: QuestionNotFound):
        log = get_logger()
        log.warning("question not found", question_id=exc.question_id, language_code=exc.language_code)

        message = f"question {exc.question_id=} not found"
        if exc.language_code:
            message = f"{exc.language_code} in {message}"

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error_message": message, "error_code": "question_not_found"},
        )

    @app.exception_handler(InvalidLanguageCode)
    async def question_invalid_language_exception_handler(request: Request, exc: InvalidLanguageCode):
        log = get_logger()
        log.warning("invalid language code", language_code=exc.language_code)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error_message": f"invalid {exc.language_code=}", "error_code": "question_format_error"},
        )

    @app.exception_handler(InvalidLimit)
    async def question_invalid_limit_exception_handler(request: Request, exc: InvalidLimit):
        log = get_logger()
        log.warning("invalid limit", limit=exc.limit, min=exc.min, max=exc.max)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error_message": f"invalid {exc.limit=} expected to be greater than {exc.min=}",
                "error_code": "query_format_error",
            },
        )
