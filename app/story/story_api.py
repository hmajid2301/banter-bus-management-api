from fastapi import APIRouter, Depends, HTTPException, status
from pydantic.error_wrappers import ValidationError
from structlog.stdlib import BoundLogger

from app.core.logger import get_logger
from app.factory import get_write_scopes
from app.game.game_exceptions import GameNotEnabledError
from app.story.story_api_models import StoryIn, StoryOut
from app.story.story_exceptions import StoryNotFound
from app.story.story_factory import get_story_service
from app.story.story_service import AbstractStoryService

router = APIRouter(
    prefix="/story",
    tags=["stories"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=StoryOut,
    response_model_exclude_none=True,
    operation_id="add_story",
)
async def add_story(
    story: StoryIn,
    story_service: AbstractStoryService = Depends(get_story_service),
    log: BoundLogger = Depends(get_logger),
):
    try:
        log.debug("trying to add new story")
        new_story = await story_service.add(story=story.dict())
        return new_story.dict()
    except GameNotEnabledError as e:
        log.warning(f"{story.game_name=} not enabled")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error_message": str(e), "error_code": "game_not_enabled"},
        )
    except (ValidationError, ValueError) as e:
        log.warning("validation error, creating story")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_message": str(e), "error_code": "story_format_error"},
        )


@router.get(
    "/{story_id}",
    status_code=status.HTTP_200_OK,
    response_model=StoryOut,
    response_model_exclude_none=True,
    operation_id="get_story",
)
async def get_story(
    story_id: str,
    story_service: AbstractStoryService = Depends(get_story_service),
    log: BoundLogger = Depends(get_logger),
):
    try:
        log = log.bind(story_id=story_id)
        log.debug("trying to get story")
        story = await story_service.get(story_id=story_id)
        return story.dict()
    except StoryNotFound:
        log.warning("story not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": f"story {story_id=} does not exist", "error_code": "story_does_not_exist"},
        )


@router.delete(
    "/{story_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_write_scopes)],
    operation_id="remove_story",
)
async def remove_story(
    story_id: str,
    story_service: AbstractStoryService = Depends(get_story_service),
    log: BoundLogger = Depends(get_logger),
):
    try:
        log = log.bind(story_id=story_id)
        log.debug("trying to delete story")
        await story_service.remove(story_id=story_id)
    except StoryNotFound:
        log.warning("story not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": f"story {story_id=} does not exist", "error_code": "story_does_not_exist"},
        )
