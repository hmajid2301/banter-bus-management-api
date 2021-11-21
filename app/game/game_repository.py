import abc
from typing import List

from app.core.repository import AbstractRepository
from app.game.game_exceptions import GameNotFoundException
from app.game.game_models import Game


class AbstractGameRepository(AbstractRepository[Game]):
    @abc.abstractmethod
    async def update_enable_status(self, game_name: str, enabled: bool) -> Game:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_game_names(self) -> List[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_game_names_filter_on_enabled_status(self, enabled: bool) -> List[str]:
        raise NotImplementedError


class GameRepository(AbstractGameRepository):
    async def add(self, game: Game):
        await Game.insert(game)

    async def get(self, game_name: str) -> Game:
        game = await Game.find_one(Game.name == game_name)
        if not game:
            raise GameNotFoundException(f"unable to find {game_name=}")
        return game

    async def remove(self, game_name: str):
        game = await self.get(game_name=game_name)
        await game.delete()

    async def get_all_game_names(self) -> List[str]:
        games = await Game.find().to_list()
        return self._get_game_names(games)

    async def get_all_game_names_filter_on_enabled_status(self, enabled: bool) -> List[str]:
        games = await Game.find(Game.enabled == enabled).to_list()
        return self._get_game_names(games)

    def _get_game_names(self, games: List[Game]):
        game_names: List[str] = []
        for game in games:
            game_names.append(game.name)
        return game_names

    async def update_enable_status(self, game_name: str, enabled: bool) -> Game:
        game = await self.get(game_name=game_name)
        game.enabled = enabled
        await game.save()
        return game
