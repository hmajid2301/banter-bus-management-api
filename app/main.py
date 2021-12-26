import uvicorn
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_health import health
from motor import motor_asyncio

from app.core.config import get_settings
from app.core.logger import get_logger, setup_logger
from app.game import game_api
from app.game.game_exceptions import add_game_exceptions
from app.game.game_models import Game
from app.middleware import catch_exceptions_middleware
from app.question import question_api
from app.question.question_exceptions import add_question_exceptions
from app.question.question_models import Question
from app.story import story_api
from app.story.story_models import Story

app = FastAPI()


@app.on_event("startup")
async def startup():
    config = get_settings()
    log = setup_logger(log_level=config.LOG_LEVEL, env=config.ENVIRONMENT)
    uri = config.get_mongodb_uri()
    client = motor_asyncio.AsyncIOMotorClient(uri)
    await init_beanie(database=client[config.DB_NAME], document_models=[Game, Story, Question])

    log = get_logger()
    log.info(f"starting banter-bus-management-api {config.WEB_HOST}:{config.WEB_PORT}")
    app.middleware("http")(catch_exceptions_middleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS,
        allow_origin_regex=config.REGEX_CORS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(game_api.router)
    app.include_router(story_api.router)
    app.include_router(question_api.router)
    app.add_api_route("/health", health([db_healthcheck]))

    add_game_exceptions(app)
    add_question_exceptions(app)


def db_healthcheck() -> bool:
    try:
        Game.find()
        return False
    except Exception:
        return False


if __name__ == "__main__":
    config = get_settings()
    uvicorn.run(app, host=config.WEB_HOST, port=config.WEB_PORT)  # type: ignore
