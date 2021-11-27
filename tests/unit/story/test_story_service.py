import uuid
from typing import List

import pytest
from pytest_mock import MockFixture

from app.game.game_service import GameService
from app.story.story_exceptions import StoryNotFound
from app.story.story_models import Story
from app.story.story_service import StoryService
from tests.unit.game.fake_game_repository import FakeGameRepository
from tests.unit.story.fake_story_repository import FakeStoryRepository
from tests.unit.story.story_service_data import (
    add_story_data,
    add_story_fail_data,
    all_games_enabled,
)


@pytest.fixture(autouse=True)
def mock_beanie_document(mocker: MockFixture):
    mocker.patch("beanie.odm.documents.Document.get_settings")


@pytest.fixture()
def game_service() -> GameService:
    from tests.data.game_collection import games

    game_repository = FakeGameRepository(games=games)
    game_service = GameService(game_repository=game_repository)
    return game_service


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "story_dict",
    add_story_data,
    ids=[
        "try to add a quibly story",
        "try to add a drawlosseum story",
        "try to add a fibbing_it story",
    ],
)
async def test_add_story(story_dict: dict, mocker: MockFixture):
    from app.game.game_models import Game

    games: List[Game] = []
    for game in all_games_enabled:
        games.append(Game(**game))

    game_repository = FakeGameRepository(games=games)
    game_service = GameService(game_repository=game_repository)
    story_repository = FakeStoryRepository(stories=[])
    story_service = StoryService(story_repository=story_repository, game_service=game_service)

    mock_uuid = mocker.patch.object(uuid, "uuid4", autospec=True)
    mock_uuid.return_value = uuid.UUID(hex="5ecd5827b6ef4067b5ac3ceac07dde9f")

    new_story = await story_service.add(story=story_dict)
    expected_story_dict = story_dict
    expected_story_dict["id"] = "5ecd5827-b6ef-4067-b5ac-3ceac07dde9f"
    assert expected_story_dict == new_story.dict(exclude_none=True)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "story_dict, expected_exception",
    add_story_fail_data,
    ids=[
        "try to add a story (missing game_name)",
        "try to add a story (invalid game_name)",
        "try to add a quibly story (invalid round)",
        "try to add a quibly story (missing round)",
        "try to add a quibly story (missing question)",
        "try to add a quibly story (missing answer)",
        "try to add a quibly story (unexpected nickname)",
        "try to add a drawlosseum story (game disabled)",
        "try to add a fibbing_it story (missing question)",
        "try to add a fibbing_it story (invalid round)",
        "try to add a fibbing_it story (missing round)",
        "try to add a fibbing_it story (unexpected nickname)",
        "try to add a drawlosseum story (missing nickname)",
    ],
)
async def test_add_story_bad_story(story_dict: dict, expected_exception, game_service: GameService):
    story_repository = FakeStoryRepository(stories=[])
    story_service = StoryService(story_repository=story_repository, game_service=game_service)

    with pytest.raises(expected_exception):
        await story_service.add(story=story_dict)


@pytest.mark.asyncio
async def test_remove_story(game_service: GameService):
    story_id = "5ecd5827-b6ef-4067-b5ac-3ceac07dde9f"
    existing_story = {
        "id": story_id,
        "game_name": "quibly",
        "question": "how many fish are there?",
        "round": "pair",
        "answers": [
            {
                "nickname": "funnyMan420",
                "answer": "one",
                "votes": 12341,
            },
            {
                "nickname": "lima_Bean",
                "answer": "many",
                "votes": 0,
            },
        ],
    }

    existing_story = Story(**existing_story)
    story_repository = FakeStoryRepository(stories=[existing_story])
    story_service = StoryService(story_repository=story_repository, game_service=game_service)

    await story_service.remove(story_id=story_id)
    with pytest.raises(StoryNotFound):
        await story_repository.get(story_id=story_id)


@pytest.mark.asyncio
async def test_remove_story_story_does_not_exist(game_service: GameService):
    story_id = "5ecd5827-b6ef-4067-b5ac-3ceac07dde9f"
    existing_story = {
        "id": story_id,
        "game_name": "quibly",
        "question": "how many fish are there?",
        "round": "pair",
        "answers": [
            {
                "nickname": "funnyMan420",
                "answer": "one",
                "votes": 12341,
            },
            {
                "nickname": "lima_Bean",
                "answer": "many",
                "votes": 0,
            },
        ],
    }

    existing_story = Story(**existing_story)
    story_repository = FakeStoryRepository(stories=[existing_story])
    story_service = StoryService(story_repository=story_repository, game_service=game_service)

    with pytest.raises(StoryNotFound):
        await story_service.remove(story_id="a-random-id")


@pytest.mark.asyncio
async def test_remove_story_story_no_stories_exist(game_service: GameService):
    story_repository = FakeStoryRepository(stories=[])
    story_service = StoryService(story_repository=story_repository, game_service=game_service)

    with pytest.raises(StoryNotFound):
        await story_service.remove(story_id="a-random-id")


@pytest.mark.asyncio
async def test_get_story(game_service: GameService):
    story_id = "5ecd5827-b6ef-4067-b5ac-3ceac07dde9f"
    existing_story = {
        "id": story_id,
        "game_name": "quibly",
        "question": "how many fish are there?",
        "round": "pair",
        "answers": [
            {
                "nickname": "funnyMan420",
                "answer": "one",
                "votes": 12341,
            },
            {
                "nickname": "lima_Bean",
                "answer": "many",
                "votes": 0,
            },
        ],
    }

    existing_story = Story(**existing_story)
    story_repository = FakeStoryRepository(stories=[existing_story])
    story_service = StoryService(story_repository=story_repository, game_service=game_service)

    story = await story_service.get(story_id=story_id)
    assert existing_story == story


@pytest.mark.asyncio
async def test_get_story_does_not_exist(game_service: GameService):
    story_repository = FakeStoryRepository(stories=[])
    story_service = StoryService(story_repository=story_repository, game_service=game_service)

    with pytest.raises(StoryNotFound):
        await story_service.get(story_id="a-random-id")
