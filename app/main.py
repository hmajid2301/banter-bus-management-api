import uvicorn
from beanie import init_beanie
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from motor import motor_asyncio

from app.core.config import get_settings
from app.core.logger import get_logger, setup_logger
from app.game import game_api
from app.game.game_exceptions import add_game_exceptions
from app.game.game_models import Game
from app.question import question_api
from app.question.question_exceptions import add_question_exceptions
from app.question.question_models import Question
from app.story import story_api
from app.story.story_models import Story

app = FastAPI()


@app.on_event("startup")
async def startup():
    config = get_settings()
    log = setup_logger(config.LOG_LEVEL)
    uri = config.get_mongodb_uri()
    client = motor_asyncio.AsyncIOMotorClient(uri)
    await init_beanie(database=client[config.DB_NAME], document_models=[Game, Story, Question])

    log = get_logger()
    log.info(f"starting banter-bus-management-api {config.WEB_HOST}:{config.WEB_PORT}")
    app.middleware("http")(catch_exceptions_middleware)
    app.include_router(game_api.router)
    app.include_router(story_api.router)
    app.include_router(question_api.router)

    add_game_exceptions(app)
    add_question_exceptions(app)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        log = get_logger()
        log.exception("failed to complete operation", request=request)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error_message": "failed to complete operation internal server error",
                "error_code": "server_error",
            },
        )


if __name__ == "__main__":
    config = get_settings()
    uvicorn.run(app, host=config.WEB_HOST, port=config.WEB_PORT)  # type: ignore
