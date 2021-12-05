from app.core.exceptions import (
    ExistsException,
    IncorrectFormatException,
    NotFoundException,
)


class QuestionNotFound(NotFoundException):
    pass


class QuestionExistsException(ExistsException):
    pass


class InvalidLanguageCode(IncorrectFormatException):
    pass


class InvalidLimit(IncorrectFormatException):
    pass
