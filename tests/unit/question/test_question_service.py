import uuid
from typing import List

import pytest
from pytest_mock import MockFixture

from app.game.game_exceptions import GameNotFound
from app.question.question_exceptions import QuestionNotFound
from app.question.question_models import Question
from app.question.question_service import QuestionService
from tests.unit.question.fake_question_repository import FakeQuestionRepository
from tests.unit.question.question_service_data import (
    add_question_data,
    add_question_data_fail,
    get_question,
)


@pytest.fixture(autouse=True)
def mock_beanie_document(mocker: MockFixture):
    mocker.patch("beanie.odm.documents.Document.get_settings")


@pytest.fixture()
def questions() -> List[Question]:
    from tests.data.question_collection import questions

    return questions


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "question_dict, expected_result",
    add_question_data,
    ids=[
        "add a quibly question, round pair",
        "add a quibly question, round answer and language de",
        "add a quibly question, round group",
        "add a drawlosseum question",
        "add a fibbing_it question, round opinion and group bike question, specify language en",
        "add a fibbing_it question, round opinion and group bike answern",
        "add a fibbing_it question, round free_form and group horse",
        "add a fibbing_it question, round likely",
    ],
)
async def test_add_question(question_dict: dict, expected_result: dict, mocker: MockFixture):
    question_repository = FakeQuestionRepository(questions=[])
    question_service = QuestionService(question_repository=question_repository)

    mock_uuid = mocker.patch.object(uuid, "uuid4", autospec=True)
    mock_uuid.return_value = uuid.UUID(hex="5ecd5827b6ef4067b5ac3ceac07dde9f")

    new_question = await question_service.add(question_dict=question_dict)
    assert expected_result == new_question.dict(exclude_none=True, by_alias=True)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "question_dict, expected_exception",
    add_question_data_fail,
    ids=[
        "try to add a quibly question, invalid round",
        "try to add a quibly question, missing round",
        "try to add a drawlosseum question, missing content",
        "try to add a fibbing_it question, invalid round",
        "try to add a fibbing_it question, round opinion, invalid type",
        "try to add a fibbing_it question, round opinion, missing group ",
        "try to add a fibbing_it_v3 question game does not exist",
        "try to add a quibly question round pair already exists",
        "try to add a quibly question round answers, language de already exists",
        "try to add a quibly question round group, language fr already exists",
        "try to add a fibbing_it question round opinions already exists",
        "try to add a fibbing_it question round free_form already exists",
        "try to add a fibbing_it question round likely already exists",
        "try to add a drawlosseum question already exists",
    ],
)
async def test_add_question_fail(question_dict: dict, expected_exception, questions: List[Question]):
    question_repository = FakeQuestionRepository(questions=questions)
    question_service = QuestionService(question_repository=question_repository)

    with pytest.raises(expected_exception):
        await question_service.add(question_dict=question_dict)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "question_id, game_name, expected_question",
    get_question,
    ids=[
        "get a quibly question",
        "get a fibbing_it question",
        "get a drawlossuem question",
    ],
)
async def test_get_question(
    question_id: str,
    game_name: str,
    expected_question: dict,
    questions: List[Question],
):
    question_repository = FakeQuestionRepository(questions=questions)
    question_service = QuestionService(question_repository=question_repository)

    question = await question_service.get(question_id=question_id, game_name=game_name)
    assert question.dict(by_alias=True, exclude_none=True) == expected_question


@pytest.mark.asyncio
async def test_get_question_does_not_exist():
    question_repository = FakeQuestionRepository(questions=[])
    question_service = QuestionService(question_repository=question_repository)

    with pytest.raises(QuestionNotFound):
        await question_service.get(question_id="a-random-id", game_name="quibly")


@pytest.mark.asyncio
async def test_get_question_game_does_not_exist(questions: List[Question]):
    question_repository = FakeQuestionRepository(questions=questions)
    question_service = QuestionService(question_repository=question_repository)

    with pytest.raises(GameNotFound):
        await question_service.get(question_id="101464a5-337f-4ce7-a4df-2b00764e5d8d", game_name="quibly_v3")


@pytest.mark.asyncio
async def test_remove_question(questions: List[Question]):
    question_repository = FakeQuestionRepository(questions=questions)
    question_service = QuestionService(question_repository=question_repository)

    question_id = "101464a5-337f-4ce7-a4df-2b00764e5d8d"
    await question_service.remove(question_id=question_id, game_name="quibly")
    with pytest.raises(QuestionNotFound):
        await question_repository.get(question_id=question_id)


@pytest.mark.asyncio
async def test_remove_question_does_not_exist(questions: List[Question]):
    question_repository = FakeQuestionRepository(questions=questions)
    question_service = QuestionService(question_repository=question_repository)

    question_id = "a-random_id"
    with pytest.raises(QuestionNotFound):
        await question_service.remove(question_id=question_id, game_name="quibly")


@pytest.mark.asyncio
async def test_remove_question_game_does_not_exist(questions: List[Question]):
    question_repository = FakeQuestionRepository(questions=questions)
    question_service = QuestionService(question_repository=question_repository)

    question_id = "101464a5-337f-4ce7-a4df-2b00764e5d8d"
    with pytest.raises(GameNotFound):
        await question_service.remove(question_id=question_id, game_name="quibly_v3")
