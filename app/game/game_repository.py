import abc

from omnibus.database.repository import AbstractRepository
from pymongo.errors import DuplicateKeyError

from app.game.game_exceptions import GameExistsException, GameNotFound
from app.game.game_models import Game


class AbstractGameRepository(AbstractRepository[Game]):
    @abc.abstractmethod
    async def update_enable_status(self, game_name: str, enabled: bool) -> Game:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_game_names(self, enabled: bool = None) -> list[str]:
        raise NotImplementedError


class GameRepository(AbstractGameRepository):
    @staticmethod
    async def add(game: Game):
        try:
            await Game.insert(game)
        except DuplicateKeyError:
            raise GameExistsException(f"game {game.name=} already exists")

    @staticmethod
    async def get(game_name: str) -> Game:
        game = await Game.find_one(Game.name == game_name)
        if not game:
            raise GameNotFound(game_name=game_name)
        return game

    async def remove(self, game_name: str):
        game = await self.get(game_name=game_name)
        await game.delete()

    async def get_all_game_names(self, enabled: bool = None) -> list[str]:
        if enabled is not None:
            games = await Game.find(Game.enabled == enabled).to_list()
        else:
            games = await Game.find().to_list()
        return self._get_game_names(games)

    # TODO: use projection https://roman-right.github.io/beanie/tutorial/finding-documents/
    @staticmethod
    def _get_game_names(games: list[Game]):
        game_names: list[str] = [game.name for game in games]
        return game_names

    async def update_enable_status(self, game_name: str, enabled: bool) -> Game:
        game = await self.get(game_name=game_name)
        game.enabled = enabled
        await game.save()
        return game
