from app.game.game_exceptions import GameExistsException, GameNotFound
from app.game.game_models import Game
from app.game.game_repository import AbstractGameRepository


class FakeGameRepository(AbstractGameRepository):
    def __init__(self, games: list[Game]):
        self.games = games

    async def add(self, new_game: Game):
        for game in self.games:
            if game.name == new_game.name:
                raise GameExistsException("game already exists")

        self.games.append(new_game)

    async def get(self, game_name: str) -> Game:
        for game in self.games:
            if game.name == game_name:
                return game

        raise GameNotFound("game not found")

    async def remove(self, game_name: str):
        game = await self.get(game_name=game_name)
        if not game:
            raise GameNotFound("game not found")
        self.games.remove(game)

    async def update_enable_status(self, game_name: str, enabled: bool) -> Game:
        for game in self.games:
            if game.name == game_name:
                game.enabled = enabled
                return game

        raise GameNotFound("game not found")

    async def get_all_game_names(self, enabled: bool = None) -> list[str]:
        names: list[str] = []
        for game in self.games:
            if enabled is not None and game.enabled == enabled:
                names.append(game.name)
            elif enabled is None:
                names.append(game.name)

        return names
