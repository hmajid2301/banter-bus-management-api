import uvicorn
from beanie import init_beanie
from fastapi import FastAPI
from motor import motor_asyncio

from app.core.config import get_settings
from app.factory import get_logger
from app.game import game_api
from app.game.game_models import Game
from app.story import story_api
from app.story.story_models import Story

app = FastAPI()


@app.on_event("startup")
async def startup():
    config = get_settings()
    uri = config.get_mongodb_uri()
    client = motor_asyncio.AsyncIOMotorClient(uri)
    await init_beanie(database=client[config.DB_NAME], document_models=[Game, Story])

    log = get_logger()
    log.info(f"starting banter-bus-management-api {config.WEB_HOST}:{config.WEB_PORT}")
    app.include_router(game_api.router)
    app.include_router(story_api.router)


if __name__ == "__main__":
    config = get_settings()
    uvicorn.run(app, host=config.WEB_HOST, port=config.WEB_PORT)
