from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.param_functions import Query
from structlog.stdlib import BoundLogger

from app.factory import get_logger, get_write_scopes
from app.game.game_api_models import GameIn, GameOut
from app.game.game_exceptions import GameExists, GameNotFound, InvalidGameFilter
from app.game.game_factory import get_game_service
from app.game.game_models import Game
from app.game.game_service import AbstractGameService

router = APIRouter(
    prefix="/game",
    tags=["games"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=GameOut,
    include_in_schema=False,
    dependencies=[Depends(get_write_scopes)],
)
async def add_game(
    game: GameIn, game_service: AbstractGameService = Depends(get_game_service), log: BoundLogger = Depends(get_logger)
):
    try:
        log = log.bind(game_name=game.name)
        log.debug("trying to add new game")
        new_game = await game_service.add(
            game_name=game.name, rules_url=game.rules_url, description=game.description, display_name=game.display_name
        )
        return new_game
    except GameExists:
        log.warning("game already exists")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error_message": f"game {game.name=} already exists", "error_code": "game_already_exists"},
        )
    except Exception:
        log.exception("failed to add new game")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_message": f"failed to add game {game.name=}", "error_code": "failed_create_game"},
        )


@router.delete(
    "/{game_name}", status_code=status.HTTP_200_OK, include_in_schema=False, dependencies=[Depends(get_write_scopes)]
)
async def remove_game(
    game_name: str,
    game_service: AbstractGameService = Depends(get_game_service),
    log: BoundLogger = Depends(get_logger),
):
    try:
        log = log.bind(game_name=game_name)
        log.debug("trying to remove existing game")
        await game_service.remove(game_name=game_name)
    except GameNotFound:
        log.warning("game not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": f"game {game_name=} does not exist", "error_code": "game_not_found"},
        )
    except Exception:
        log.exception("failed to remove existing game")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_message": f"failed to remove game {game_name=}", "error_code": "failed_remove_game"},
        )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[str],
)
async def get_all_game_names(
    filter: Optional[str] = Query("all", alias="status"),
    game_service: AbstractGameService = Depends(get_game_service),
    log: BoundLogger = Depends(get_logger),
) -> List[str]:
    try:
        log.debug("trying to get all game names")
        if not filter:
            filter = "all"

        game_names = await game_service.get_game_names(filter=filter)
        return game_names
    except InvalidGameFilter as e:
        log.warning("invalid game", filter=filter)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_message": str(e), "error_code": "invalid_status"},
        )
    except Exception:
        log.exception("failed to get all game names")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_message": "failed to get all game names", "error_code": "failed_get_game_names"},
        )


@router.get(
    "/{game_name}",
    status_code=status.HTTP_200_OK,
    response_model=GameOut,
)
async def get_game(
    game_name: str,
    game_service: AbstractGameService = Depends(get_game_service),
    log: BoundLogger = Depends(get_logger),
):
    try:
        log = log.bind(game_name=game_name)
        log.debug("trying to get game")
        game = await game_service.get(game_name=game_name)
        return game
    except GameNotFound:
        log.warning("game not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": f"game {game_name=} does not exist", "error_code": "game_not_found"},
        )
    except Exception:
        log.exception("failed to get game")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_message": f"failed to get game {game_name=}", "error_code": "failed_get_game"},
        )


@router.put(
    "/{game_name}:enable",
    status_code=status.HTTP_200_OK,
    response_model=GameOut,
    dependencies=[Depends(get_write_scopes)],
)
async def enable_game(
    game_name: str,
    game_service: AbstractGameService = Depends(get_game_service),
    log: BoundLogger = Depends(get_logger),
):
    game = await _update_enable_status(game_name=game_name, game_service=game_service, log=log, enabled=True)
    return game


@router.put(
    "/{game_name}:disable",
    status_code=status.HTTP_200_OK,
    response_model=GameOut,
    dependencies=[Depends(get_write_scopes)],
)
async def disabled_game(
    game_name: str,
    game_service: AbstractGameService = Depends(get_game_service),
    log: BoundLogger = Depends(get_logger),
):
    game = await _update_enable_status(game_name=game_name, game_service=game_service, log=log, enabled=False)
    return game


async def _update_enable_status(
    game_name: str, game_service: AbstractGameService, log: BoundLogger, enabled: bool
) -> Game:
    try:
        log = log.bind(game_name=game_name)
        log.debug(f"trying to update enable status  to {enabled=}")
        game = await game_service.update_enabled_status(game_name=game_name, enabled=enabled)
        return game
    except GameNotFound:
        log.warning("game not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": f"game {game_name=} does not exist", "error_code": "game_not_found"},
        )
    except Exception:
        log.exception("failed to update game enabled status")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_message": f"failed to update game {game_name=} enabled status to {enabled=}",
                "error_code": "failed_update_game_enable",
            },
        )
