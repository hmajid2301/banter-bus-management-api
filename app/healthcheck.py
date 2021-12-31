from app.game.game_models import Game


def db_healthcheck() -> bool:
    try:
        Game.find()
        return False
    except Exception:
        return False
