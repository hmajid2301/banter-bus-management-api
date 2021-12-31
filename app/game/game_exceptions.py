from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from omnibus.log.logger import get_logger

from app.core.exceptions import ExistsException, InvalidFilter, NotFoundException


class GameNotFound(NotFoundException):
    def __init__(self, game_name: str) -> None:
        self.game_name = game_name


class GameExistsException(ExistsException):
    pass


class InvalidGameFilter(InvalidFilter):
    pass


class GameNotEnabledError(Exception):
    pass


def add_game_exceptions(app: FastAPI):
    @app.exception_handler(GameNotFound)
    async def game_not_found_exception_handler(request: Request, exc: GameNotFound):
        log = get_logger()
        log.warning("game not found", game_name=exc.game_name)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error_message": f"game {exc.game_name=} not found", "error_code": "game_not_found"},
        )
