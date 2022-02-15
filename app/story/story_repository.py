from omnibus.database.repository import AbstractRepository
from pymongo.errors import DuplicateKeyError

from app.story.story_exceptions import StoryExistsException, StoryNotFound
from app.story.story_models import Story


class AbstractStoryRepository(AbstractRepository[Story]):
    pass


class StoryRepository(AbstractStoryRepository):
    @staticmethod
    async def add(story: Story):
        try:
            await Story.insert(story)
        except DuplicateKeyError:
            raise StoryExistsException(f"story {story.story_id=} already exists")

    @staticmethod
    async def get(story_id: str) -> Story:
        story = await Story.find_one(Story.story_id == story_id)
        if not story:
            raise StoryNotFound(f"unable to find {story_id=}")
        return story

    async def remove(self, story_id: str):
        await self.get(story_id=story_id)
        await Story.find_one(Story.story_id == story_id).delete()
