import uuid
from typing import Any

from app.game.games.game import get_game
from app.story.story_models import Story
from app.story.story_repository import AbstractStoryRepository


class StoryService:
    def __init__(self, story_repository: AbstractStoryRepository):
        self.story_repository = story_repository

    async def add(self, story: dict[Any, Any]) -> Story:
        id_ = str(uuid.uuid4())
        new_story = Story(**story, story_id=id_)
        self._validate_story(story=new_story)

        await self.story_repository.add(new_story)
        return new_story

    @staticmethod
    def _validate_story(story: Story):
        game_name = story.game_name
        game = get_game(game_name=game_name)
        game.validate_story(nickname=story.nickname or "", round_=story.round_ or "", answers=story.answers)

    async def remove(self, story_id: str):
        await self.story_repository.remove(story_id)

    async def get(self, story_id: str) -> Story:
        story = await self.story_repository.get(story_id)
        return story
