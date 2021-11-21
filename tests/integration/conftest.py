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
    from tests.integration.data.game_collection import games

    await Game.insert_many(documents=games)
    yield
    await Game.delete_all()
