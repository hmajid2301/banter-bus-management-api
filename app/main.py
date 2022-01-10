from fastapi import FastAPI
from omnibus.app import setup_app
from omnibus.middleware.exceptions import catch_exceptions_http
from omnibus.operation_id import use_route_names_as_operation_ids

from app.core.config import get_settings
from app.game import game_api
from app.game.game_exceptions import add_game_exceptions
from app.game.game_models import Game
from app.healthcheck import db_healthcheck
from app.question import question_api
from app.question.question_exceptions import add_question_exceptions
from app.question.question_models import Question
from app.story import story_api
from app.story.story_models import Story

app = FastAPI(title="banter-bus-management-api")


@app.on_event("startup")
async def startup():
    await setup_app(
        app=app, get_settings=get_settings, document_models=[Game, Story, Question], healthcheck=db_healthcheck
    )
    app.middleware("http")(catch_exceptions_http)

    app.include_router(game_api.router)
    app.include_router(story_api.router)
    app.include_router(question_api.router)
    use_route_names_as_operation_ids(app)

    add_game_exceptions(app)
    add_question_exceptions(app)
