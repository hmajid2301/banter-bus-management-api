from fastapi import Depends

from app.game.game_repository import AbstractGameRepository, GameRepository
from app.game.game_service import GameService


def get_game_repository() -> AbstractGameRepository:
    return GameRepository()


def get_game_service(
    game_repository: AbstractGameRepository = Depends(get_game_repository),
) -> GameService:
    game_service = GameService(game_repository=game_repository)
    return game_service
