import abc
import uuid

from app.game.games.game import get_game
from app.story.story_models import Story
from app.story.story_repository import AbstractStoryRepository


class AbstractStoryService(abc.ABC):
    @abc.abstractmethod
    async def add(self, story: dict) -> Story:
        raise NotImplementedError

    @abc.abstractmethod
    async def remove(self, story_id: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, story_id: str) -> Story:
        raise NotImplementedError


class StoryService(AbstractStoryService):
    def __init__(self, story_repository: AbstractStoryRepository):
        self.story_repository = story_repository

    async def add(self, story: dict) -> Story:
        id_ = str(uuid.uuid4())
        new_story = Story(**story, story_id=id_)
        self._validate_story(story=new_story)

        await self.story_repository.add(new_story)
        return new_story

    def _validate_story(self, story: Story):
        game_name = story.game_name
        game = get_game(game_name=game_name)
        game.validate_story(nickname=story.nickname or "", round_=story.round_ or "", answers=story.answers)

    async def remove(self, story_id: str):
        await self.story_repository.remove(story_id)

    async def get(self, story_id: str) -> Story:
        story = await self.story_repository.get(story_id)
        return story
