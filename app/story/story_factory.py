from fastapi import Depends

from app.game.game_factory import get_game_service
from app.game.game_service import AbstractGameService
from app.story.story_repository import AbstractStoryRepository, StoryRepository
from app.story.story_service import AbstractStoryService, StoryService


def get_story_repository() -> AbstractStoryRepository:
    return StoryRepository()


def get_story_service(
    story_repository: AbstractStoryRepository = Depends(get_story_repository),
    game_service: AbstractGameService = Depends(get_game_service),
) -> AbstractStoryService:
    story_service = StoryService(story_repository=story_repository, game_service=game_service)
    return story_service
