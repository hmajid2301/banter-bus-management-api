import abc

from beanie.operators import GT, Exists
from omnibus.database.repository import AbstractRepository
from pymongo.errors import DuplicateKeyError

from app.question.question_exceptions import QuestionExistsException, QuestionNotFound
from app.question.question_models import NewQuestion, Question


class AbstractQuestionRepository(AbstractRepository[Question]):
    @abc.abstractmethod
    async def does_question_exist(self, new_question: NewQuestion) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_enable_status(self, question_id: str, enabled: bool) -> Question:
        raise NotImplementedError

    @abc.abstractmethod
    async def add_translation(self, question_id: str, language_code: str, content: str) -> Question:
        raise NotImplementedError

    @abc.abstractmethod
    async def remove_translation(self, question_id: str, language_code: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_ids(self, game_name: str, limit: int, cursor: str | None = None) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_random(self, game_name: str, round_: str, language_code: str, limit: int) -> list[Question]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_questions_in_group(
        self, game_name: str, round_: str, language_code: str, group_name: str
    ) -> list[Question]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_groups(self, game_name: str, round_: str, minimum_questions: int) -> list[str]:
        raise NotImplementedError


class QuestionRepository(AbstractQuestionRepository):
    @staticmethod
    async def add(question: Question):
        try:
            await Question.insert(question)
        except DuplicateKeyError:
            raise QuestionExistsException(f"question {question.question_id=} already exists")

    @staticmethod
    async def get(question_id: str) -> Question:
        question = await Question.find_one(Question.question_id == question_id)
        if not question:
            raise QuestionNotFound(question_id=question_id)

        return question

    async def remove(self, question_id: str):
        await self.get(question_id=question_id)
        await Question.find_one(Question.question_id == question_id).delete()

    async def does_question_exist(self, new_question: NewQuestion) -> bool:
        questions: list[Question] = await Question.find(
            Question.round_ == new_question.round_,
            Question.game_name == new_question.game_name,
            Question.group == new_question.group,
        ).to_list()

        for question in questions:
            try:
                content = question.content[new_question.language_code]
                if content == new_question.content:
                    return True
            except KeyError:
                continue

        return False

    async def update_enable_status(self, question_id: str, enabled: bool) -> Question:
        question = await self.get(question_id=question_id)
        question.enabled = enabled
        await question.save()
        return question

    async def add_translation(self, question_id: str, language_code: str, content: str) -> Question:
        question = await self.get(question_id=question_id)
        if language_code in question.content:
            raise QuestionExistsException(f"question translation {language_code=} already exists for {question_id=}")
        question.content[language_code] = content
        await question.save()
        return question

    async def remove_translation(self, question_id: str, language_code: str):
        question = await self.get(question_id=question_id)
        try:
            del question.content[language_code]
        except KeyError:
            raise QuestionNotFound(question_id=question_id, language_code=language_code)
        await question.save()

    async def get_ids(self, game_name: str, limit: int, cursor: str | None = None) -> list[str]:
        questions = (
            await Question.find(Question.game_name == game_name, GT(Question.question_id, cursor))
            .limit(limit)
            .to_list()
        )
        question_ids = [question.question_id for question in questions]
        return question_ids

    @staticmethod
    async def get_random(game_name: str, round_: str, language_code: str, limit: int) -> list[Question]:
        questions = (
            await Question.find(
                Question.game_name == game_name,
                Question.round_ == round_,
                Question.enabled == True,  # noqa
                Exists(Question.content[language_code], True),
            )
            .aggregate(
                [
                    {
                        "$sample": {"size": limit},
                    },
                ],
                projection_model=Question,
            )
            .to_list()
        )

        return questions

    @staticmethod
    async def get_questions_in_group(
        game_name: str, round_: str, language_code: str, group_name: str
    ) -> list[Question]:
        questions = await Question.find(
            Question.game_name == game_name,
            Question.round_ == round_,
            Question.group.name == group_name,  # type: ignore
            Question.enabled == True,  # noqa
            Exists(Question.content[language_code], True),
        ).to_list()
        return questions

    async def get_groups(self, game_name: str, round_: str, minimum_questions: int) -> list[str]:
        # TODO: move to when fixed https://github.com/roman-right/beanie/issues/133
        question_groups = (
            await Question.find(Question.game_name == game_name, Question.round_ == round_)
            .aggregate(
                [
                    {
                        "$group": {
                            "_id": "$group.name",
                            "count": {"$sum": 1},
                        },
                    },
                    {"$match": {"count": {"$gte": minimum_questions}}},
                ],
            )
            .to_list()
        )
        groups: list[str] = []
        for group in question_groups:
            if group["_id"] is not None:
                groups.append(group["_id"])

        return groups
