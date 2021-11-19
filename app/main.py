from fastapi import FastAPI

from .games import api as game_api

app = FastAPI()
app.include_router(game_api.router)
