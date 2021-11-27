from app.core.exceptions import (
    ExistsException,
    IncorrectFormatException,
    NotFoundException,
)


class StoryNotFound(NotFoundException):
    pass


class StoryExists(ExistsException):
    pass


class StoryIncorrectFormatException(IncorrectFormatException):
    pass
