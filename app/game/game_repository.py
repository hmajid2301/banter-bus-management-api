import abc
from typing import List

from omnibus.database.repository import AbstractRepository
from pymongo.errors import DuplicateKeyError

from app.game.game_exceptions import GameExistsException, GameNotFound
from app.game.game_models import Game


class AbstractGameRepository(AbstractRepository[Game]):
    @abc.abstractmethod
    async def update_enable_status(self, game_name: str, enabled: bool) -> Game:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_game_names(self, enabled: bool = None) -> List[str]:
        raise NotImplementedError


class GameRepository(AbstractGameRepository):
    async def add(self, game: Game):
        try:
            await Game.insert(game)
        except DuplicateKeyError:
            raise GameExistsException(f"game {game.name=} already exists")

    async def get(self, game_name: str) -> Game:
        game = await Game.find_one(Game.name == game_name)
        if not game:
            raise GameNotFound(game_name=game_name)
        return game

    async def remove(self, game_name: str):
        game = await self.get(game_name=game_name)
        await game.delete()

    async def get_all_game_names(self, enabled: bool = None) -> List[str]:
        if enabled is not None:
            games = await Game.find(Game.enabled == enabled).to_list()
        else:
            games = await Game.find().to_list()
        return self._get_game_names(games)

    # TODO: use projection https://roman-right.github.io/beanie/tutorial/finding-documents/
    def _get_game_names(self, games: List[Game]):
        game_names: List[str] = [game.name for game in games]
        return game_names

    async def update_enable_status(self, game_name: str, enabled: bool) -> Game:
        game = await self.get(game_name=game_name)
        game.enabled = enabled
        await game.save()
        return game
