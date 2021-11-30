import pytest
from fastapi import status
from httpx import AsyncClient

from app.question.question_models import Question
from tests.integration.data.question_test_data import (
    add_question_data,
    add_question_translation_data,
    delete_question_translation,
    disabled_question_data,
    enabled_question_data,
    get_question_data,
    get_question_translation_data,
    remove_question_data,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "game_name, request_data, expected_status_code, expected_result",
    add_question_data,
    ids=[
        "add a quibly question",
        "add a drawlosseum question",
        "add a fibbing_it question",
        "try to add a question to a game that does not exist",
        "try to add a quibly question that already exists",
        "try to add a fibbing_it question that already exists",
        "try to add a drawlosseum question that already exists",
        "try to add an invalid drawlosseum question",
        "try to add an invalid fibbing_it question",
        "try to add an invalid quibly question",
        "try to add an invalid language code question",
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
        "get a drawlosseum question",
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
        "remove a drawlosseum question",
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
        question = await Question.find_one(Question.question_id == question_id)
        assert question is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "game_name, question_id, expected_status_code, expected_result",
    enabled_question_data,
    ids=[
        "enable a disabled question",
        "enable an enabled question",
        "try to enable question, id does not exist",
        "try to enable question, game does not exist",
    ],
)
async def test_enable_game(
    client: AsyncClient, game_name: str, question_id: str, expected_status_code: int, expected_result: dict
):
    url = f"/game/{game_name}/question/{question_id}:enable"
    response = await client.put(url)
    assert response.status_code == expected_status_code

    if response.status_code == status.HTTP_200_OK:
        assert response.json() == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "game_name, question_id, expected_status_code, expected_result",
    disabled_question_data,
    ids=[
        "disable an enabled question",
        "disable an disabled question",
        "try to disable question, id does not exist",
        "try to disable question, game does not exist",
    ],
)
async def test_disable_game(
    client: AsyncClient, game_name: str, question_id: str, expected_status_code: int, expected_result: dict
):
    url = f"/game/{game_name}/question/{question_id}:disable"
    response = await client.put(url)
    assert response.status_code == expected_status_code

    if response.status_code == status.HTTP_200_OK:
        assert response.json() == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "game_name, question_id, language_code, request_data, expected_status_code, expected_result",
    add_question_translation_data,
    ids=[
        "add a quibly question",
        "add a fibbing_it question",
        "add a drawlosseum question",
        "try to add a question (game not found)",
        "try to add a question (question not found)",
        "try to add a question (language code exists)",
        "try to add a question (invalid language code)",
    ],
)
async def test_add_question_translation(
    client: AsyncClient,
    game_name: str,
    question_id: str,
    language_code: str,
    request_data: str,
    expected_status_code: int,
    expected_result: dict,
):
    url = f"/game/{game_name}/question/{question_id}/{language_code}"
    response = await client.post(url, json=request_data)
    assert response.status_code == expected_status_code

    if response.status_code == status.HTTP_201_CREATED:
        assert response.json() == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "game_name, question_id, language_code, expected_status_code, expected_result",
    get_question_translation_data,
    ids=[
        "get a quibly question",
        "get a fibbing_it question",
        "get a drawlosseum question",
        "try to get a question (game not found)",
        "try to get a question (question not found)",
        "try to get a question (invalid language code)",
    ],
)
async def test_get_question_translation(
    client: AsyncClient,
    game_name: str,
    question_id: str,
    language_code: str,
    expected_status_code: int,
    expected_result: dict,
):
    url = f"/game/{game_name}/question/{question_id}/{language_code}"
    response = await client.get(url)
    assert response.status_code == expected_status_code

    if response.status_code == status.HTTP_200_OK:
        assert response.json() == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "game_name, question_id, language_code, expected_status_code, expected_result",
    delete_question_translation,
    ids=[
        "remove a quibly question",
        "remove a fibbing_it question",
        "remove a drawlosseum question",
        "try to remove a question (game not found)",
        "try to remove a question (question not found)",
        "try to remove a question (invalid language code)",
    ],
)
async def test_remove_question_translation(
    client: AsyncClient,
    game_name: str,
    question_id: str,
    language_code: str,
    expected_status_code: int,
    expected_result: dict,
):
    url = f"/game/{game_name}/question/{question_id}/{language_code}"
    response = await client.delete(url)
    assert response.status_code == expected_status_code

    if response.status_code == status.HTTP_200_OK:
        question = await Question.find_one(Question.question_id == question_id)
        assert question is not None
        question_dict = question.dict(by_alias=True, exclude_none=True)
        del question_dict["_id"]
        assert question_dict == expected_result


def _clean_response(response: dict):
    del response["question_id"]
    return response
