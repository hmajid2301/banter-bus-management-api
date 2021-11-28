from fastapi import APIRouter, Depends, HTTPException, status
from pydantic.error_wrappers import ValidationError
from structlog.stdlib import BoundLogger

from app.factory import get_logger
from app.game.game_exceptions import GameNotEnabledError, GameNotFound
from app.story.story_api_models import StoryIn, StoryOut
from app.story.story_exceptions import StoryNotFound
from app.story.story_factory import get_story_service
from app.story.story_service import AbstractStoryService

router = APIRouter(
    prefix="/story",
    tags=["stories"],
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=StoryOut, response_model_exclude_none=True)
async def add_story(
    story: StoryIn,
    story_service: AbstractStoryService = Depends(get_story_service),
    log: BoundLogger = Depends(get_logger),
):
    try:
        log.debug("trying to add new story")
        new_story = await story_service.add(story=story.dict())
        return new_story.dict()
    except GameNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": str(e), "error_code": "game_not_found"},
        )
    except GameNotEnabledError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error_message": str(e), "error_code": "game_not_enabled"},
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_message": str(e), "error_code": "story_format_error"},
        )
    except Exception:
        log.exception("failed to add new story")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_message": f"failed to add story {story.game_name=}", "error_code": "failed_create_story"},
        )


@router.get("/{story_id}", status_code=status.HTTP_200_OK, response_model=StoryOut, response_model_exclude_none=True)
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
        log.warning("failed to get story, it does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": f"story {story_id=} does not exist", "error_code": "story_does_not_exist"},
        )
    except Exception:
        log.exception("failed to get story")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_message": f"failed to get story {story_id=}", "error_code": "failed_get_story"},
        )


@router.delete(
    "/{story_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_story(
    story_id: str,
    story_service: AbstractStoryService = Depends(get_story_service),
    log: BoundLogger = Depends(get_logger),
):
    try:
        log = log.bind(story_id=story_id)
        log.debug("trying to delete story")
        await story_service.remove(story_id=story_id)
    except StoryNotFound:
        log.warning("failed to delete story, it does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_message": f"story {story_id=} does not exist", "error_code": "story_does_not_exist"},
        )
    except Exception:
        log.exception("failed to delete story")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_message": f"failed to delete story {story_id=}", "error_code": "failed_remove_story"},
        )
