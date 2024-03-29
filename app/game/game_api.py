from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.param_functions import Query
from omnibus.log.logger import get_logger
from structlog.stdlib import BoundLogger

from app.auth import get_auth
from app.game.game_api_models import GameIn, GameOut
from app.game.game_exceptions import GameExistsException, InvalidGameFilter
from app.game.game_factory import get_game_service
from app.game.game_models import Game
from app.game.game_service import GameService

router = APIRouter(
    prefix="/game",
    tags=["games"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=GameOut,
    include_in_schema=False,
    dependencies=[Depends(get_auth())],
)
async def add_game(
    game: GameIn, game_service: GameService = Depends(get_game_service), log: BoundLogger = Depends(get_logger)
):
    try:
        log = log.bind(game_name=game.name)
        log.debug("trying to add new game")
        new_game = await game_service.add(
            game_name=game.name,
            rules_url=game.rules_url,
            description=game.description,
            display_name=game.display_name,
            minimum_players=game.minimum_players,
            maximum_players=game.maximum_players,
        )
        return new_game
    except GameExistsException:
        log.warning("game already exists")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error_message": f"game {game.name=} already exists", "error_code": "game_already_exists"},
        )


@router.delete(
    "/{game_name}",
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
    dependencies=[Depends(get_auth())],
)
async def remove_game(
    game_name: str,
    game_service: GameService = Depends(get_game_service),
    log: BoundLogger = Depends(get_logger),
):
    log = log.bind(game_name=game_name)
    log.debug("trying to remove existing game")
    await game_service.remove(game_name=game_name)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[str],
)
async def get_all_game_names(
    enabled_filter: str | None = Query("all", alias="status"),
    game_service: GameService = Depends(get_game_service),
    log: BoundLogger = Depends(get_logger),
) -> list[str]:
    try:
        log.debug("trying to get all game names")
        if not enabled_filter:
            enabled_filter = "all"

        game_names = await game_service.get_game_names(enabled_filter=enabled_filter)
        return game_names
    except InvalidGameFilter as e:
        log.warning("invalid game", filter=enabled_filter)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_message": str(e), "error_code": "invalid_status"},
        )


@router.get(
    "/{game_name}",
    status_code=status.HTTP_200_OK,
    response_model=GameOut,
)
async def get_game(
    game_name: str,
    game_service: GameService = Depends(get_game_service),
    log: BoundLogger = Depends(get_logger),
):
    log = log.bind(game_name=game_name)
    log.debug("trying to get game")
    game = await game_service.get(game_name=game_name)
    return game


@router.put(
    "/{game_name}:enable",
    status_code=status.HTTP_200_OK,
    response_model=GameOut,
    dependencies=[Depends(get_auth())],
)
async def enable_game(
    game_name: str,
    game_service: GameService = Depends(get_game_service),
    log: BoundLogger = Depends(get_logger),
):
    game = await _update_enable_status(game_name=game_name, game_service=game_service, log=log, enabled=True)
    return game


@router.put(
    "/{game_name}:disable",
    status_code=status.HTTP_200_OK,
    response_model=GameOut,
    dependencies=[Depends(get_auth())],
)
async def disabled_game(
    game_name: str,
    game_service: GameService = Depends(get_game_service),
    log: BoundLogger = Depends(get_logger),
):
    game = await _update_enable_status(game_name=game_name, game_service=game_service, log=log, enabled=False)
    return game


async def _update_enable_status(game_name: str, game_service: GameService, log: BoundLogger, enabled: bool) -> Game:
    log = log.bind(game_name=game_name)
    log.debug(f"trying to update enable status  to {enabled=}")
    game = await game_service.update_enabled_status(game_name=game_name, enabled=enabled)
    return game
