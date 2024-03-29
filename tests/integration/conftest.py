from typing import AsyncIterator

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from app.main import application


@pytest.fixture()
async def client() -> AsyncIterator[AsyncClient]:
    async with LifespanManager(application):
        async with AsyncClient(app=application, base_url="http://localhost") as client:
            yield client


@pytest.fixture(autouse=True)
async def setup_and_teardown(client):
    from app.game.game_models import Game
    from app.question.question_models import Question
    from app.story.story_models import Story
    from tests.data.game_collection import games
    from tests.data.question_collection import questions
    from tests.data.story_collection import stories

    try:
        await Game.insert_many(documents=games)
        await Story.insert_many(documents=stories)
        await Question.insert_many(documents=questions)
    except Exception as e:
        print("Failed", e)
    yield
    await Game.delete_all()
    await Story.delete_all()
    await Question.delete_all()
