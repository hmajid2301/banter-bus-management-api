from app.core.repository import AbstractRepository
from app.story.story_exceptions import StoryNotFoundException
from app.story.story_models import Story


class AbstractStoryRepository(AbstractRepository[Story]):
    pass


class StoryRepository(AbstractStoryRepository):
    async def add(self, story: Story):
        await Story.insert(story)

    async def get(self, story_id: str) -> Story:
        story = await Story.find_one(Story.id == story_id)
        if not story:
            raise StoryNotFoundException(f"unable to find {story_id=}")
        return story

    async def remove(self, story_id: str):
        story = await self.get(story_id=story_id)
        await story.delete()
