from pymongo.errors import DuplicateKeyError

from app.core.repository import AbstractRepository
from app.story.story_exceptions import StoryExists, StoryNotFound
from app.story.story_models import Story


class AbstractStoryRepository(AbstractRepository[Story]):
    pass


class StoryRepository(AbstractStoryRepository):
    async def add(self, story: Story):
        try:
            await Story.insert(story)
        except DuplicateKeyError:
            raise StoryExists(f"story {story.story_id=} already exists")

    async def get(self, story_id: str) -> Story:
        story = await Story.find_one(Story.story_id == story_id)
        if not story:
            raise StoryNotFound(f"unable to find {story_id=}")
        return story

    async def remove(self, story_id: str):
        await self.get(story_id=story_id)
        await Story.find_one(Story.story_id == story_id).delete()
