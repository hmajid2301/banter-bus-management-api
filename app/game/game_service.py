import abc
from typing import Dict, List

from pymongo.errors import DuplicateKeyError

from app.game.game_exceptions import GameExists, InvalidGameFilter
from app.game.game_models import Game
from app.game.game_repository import AbstractGameRepository


class AbstractGameService(abc.ABC):
    @abc.abstractmethod
    async def add(self, name: str, rules_url: str, description: str, display_name: str) -> Game:
        raise NotImplementedError

    @abc.abstractmethod
    async def remove(self, name: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, name: str) -> Game:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_game_names(self, filter: str) -> List[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_enabled_status(self, game_name: str, enabled: bool) -> Game:
        raise NotImplementedError


class GameService(AbstractGameService):
    def __init__(self, game_repository: AbstractGameRepository):
        self.game_repository = game_repository

    async def add(self, name: str, rules_url: str, description: str, display_name: str) -> Game:
        try:
            new_game = Game(
                name=name, rules_url=rules_url, enabled=True, description=description, display_name=display_name
            )
            await self.game_repository.add(new_game)
            return new_game
        except DuplicateKeyError:
            raise GameExists(f"game {name=} already exists")

    async def remove(self, name: str):
        await self.game_repository.remove(name)

    async def get(self, name: str) -> Game:
        game = await self.game_repository.get(name)
        return game

    async def get_game_names(self, filter: str) -> List[str]:
        filter_map: Dict[str, List[str]] = {
            "all": await self.game_repository.get_all_game_names(),
            "enabled": await self.game_repository.get_all_game_names_filter_on_enabled_status(enabled=True),
            "disabled": await self.game_repository.get_all_game_names_filter_on_enabled_status(enabled=False),
        }

        try:
            game_names = filter_map[filter]
            return game_names
        except KeyError:
            raise InvalidGameFilter(f"invalid {filter=} must be one of {', '.join(filter_map.keys())}")

    async def update_enabled_status(self, game_name: str, enabled: bool) -> Game:
        game = await self.game_repository.update_enable_status(game_name=game_name, enabled=enabled)
        return game
