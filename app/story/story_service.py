import abc
import uuid

from pymongo.errors import DuplicateKeyError

from app.game.game_exceptions import GameNotEnabledError
from app.game.game_service import AbstractGameService
from app.story.story_exceptions import StoryExists
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
    def __init__(self, story_repository: AbstractStoryRepository, game_service: AbstractGameService):
        self.story_repository = story_repository
        self.game_service = game_service

    async def add(self, story: dict) -> Story:
        id_ = str(uuid.uuid4())
        try:
            new_story = Story(**story, id=id_)
            game = await self.game_service.get(name=new_story.game_name)
            if not game.enabled:
                raise GameNotEnabledError(f"expected game {new_story.game_name=} to be enabled to add a new story")

            await self.story_repository.add(new_story)
            return new_story
        except DuplicateKeyError:
            raise StoryExists(f"story {id_=} already exists")

    async def remove(self, story_id: str):
        await self.story_repository.remove(story_id)

    async def get(self, story_id: str) -> Story:
        story = await self.story_repository.get(story_id)
        return story
