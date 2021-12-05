from typing import Dict

from app.game.game_exceptions import GameNotFound
from app.game.games.abstract_game import AbstractGame
from app.game.games.drawlosseum import DrawlosseumGame
from app.game.games.fibbing_it import FibbingItGame
from app.game.games.quibly import QuiblyGame


def get_game(game_name: str) -> AbstractGame:
    valid_games: Dict[str, AbstractGame] = {
        "quibly": QuiblyGame(),
        "fibbing_it": FibbingItGame(),
        "drawlosseum": DrawlosseumGame(),
    }

    try:
        game = valid_games[game_name]
    except KeyError:
        raise GameNotFound(f"game {game_name=} not found")

    return game
