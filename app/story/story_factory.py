from fastapi import Depends

from app.story.story_repository import AbstractStoryRepository, StoryRepository
from app.story.story_service import AbstractStoryService, StoryService


def get_story_repository() -> AbstractStoryRepository:
    return StoryRepository()


def get_story_service(
    story_repository: AbstractStoryRepository = Depends(get_story_repository),
) -> AbstractStoryService:
    story_service = StoryService(story_repository=story_repository)
    return story_service
