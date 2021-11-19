from typing import List, Optional

from fastapi import APIRouter, status

from .api_models import GameIn, GameOut

router = APIRouter(
    prefix="/game",
    tags=["games"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=GameOut,
)
async def create_game(game: GameIn):
    pass


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[str],
)
async def get_games(enabled: Optional[bool] = None):
    pass


@router.get(
    "/{game_name}",
    status_code=status.HTTP_200_OK,
    response_model=GameOut,
)
async def get_game(game_name: str):
    pass


@router.put(
    "/{game_name}:enabled",
    status_code=status.HTTP_200_OK,
    response_model=GameOut,
)
async def enable_game(game_name: str):
    pass


@router.put(
    "/{game_name}:disabled",
    status_code=status.HTTP_200_OK,
    response_model=GameOut,
)
async def disabled_game(game_name: str):
    pass


@router.delete(
    "/{game_name}",
    status_code=status.HTTP_200_OK,
    response_model=GameOut,
)
async def delete_game(game_name: str):
    pass
