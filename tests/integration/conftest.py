from typing import AsyncIterator

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from app.main import app


@pytest.fixture()
async def client() -> AsyncIterator[AsyncClient]:
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://localhost") as client:
            yield client


@pytest.fixture(autouse=True)
async def setup_and_teardown(client):
    from app.game.game_models import Game
    from app.story.story_models import Story
    from tests.integration.data.game_collection import games
    from tests.integration.data.story_collection import stories

    try:
        await Game.insert_many(documents=games)
        await Story.insert_many(documents=stories)
    except Exception as e:
        print("Failed", e)
    yield
    await Game.delete_all()
    await Story.delete_all()
