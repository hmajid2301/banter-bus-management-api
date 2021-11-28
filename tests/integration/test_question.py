import pytest
from fastapi import status
from httpx import AsyncClient

from app.question.question_models import Question
from tests.integration.data.question_test_data import (
    add_question_data,
    get_question_data,
    remove_question_data,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "game_name, request_data, expected_status_code, expected_result",
    add_question_data,
    ids=[
        "add a quibly question",
        "add a drawlossuem question",
        "add a fibbing_it question",
        "try to add a question to a game that does not exist",
        "try to add a quibly question that already exists",
        "try to add a fibbing_it question that already exists",
        "try to add a drawlossuem question that already exists",
        "try to add an invalid drawlossuem question",
        "try to add an invalid fibbing_it question",
        "try to add an invalid quibly question",
    ],
)
async def test_add_question(
    client: AsyncClient, game_name: str, request_data: dict, expected_status_code: int, expected_result: dict
):
    url = f"/game/{game_name}/question"
    response = await client.post(url, json=request_data)
    assert response.status_code == expected_status_code

    if response.status_code == status.HTTP_201_CREATED:
        clean_response = _clean_response(response.json())
        assert clean_response == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "game_name, question_id, expected_status_code, expected_result",
    get_question_data,
    ids=[
        "get a quibly question",
        "get a drawlossuem question",
        "get a fibbing_it question",
        "get a question which does not exist",
        "get a question where game does not exist",
    ],
)
async def test_get_question(
    client: AsyncClient, game_name: str, question_id: dict, expected_status_code: int, expected_result: dict
):
    url = f"/game/{game_name}/question/{question_id}"
    response = await client.get(url)
    assert response.status_code == expected_status_code

    if response.status_code == status.HTTP_200_OK:
        assert response.json() == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "game_name, question_id, expected_status_code",
    remove_question_data,
    ids=[
        "remove a quibly question",
        "remove a drawlossuem question",
        "remove a fibbing_it question",
        "remove a question which does not exist",
        "remove a question where game does not exist",
    ],
)
async def test_remove_question(client: AsyncClient, game_name: str, question_id: dict, expected_status_code: int):
    url = f"/game/{game_name}/question/{question_id}"
    response = await client.delete(url)
    assert response.status_code == expected_status_code

    if response.status_code == status.HTTP_200_OK:
        question = await Question.find_one(Question.id == question_id)
        assert question is None


def _clean_response(response: dict):
    del response["id"]
    return response
