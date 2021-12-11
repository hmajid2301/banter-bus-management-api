from app.core.exceptions import (
    ExistsException,
    IncorrectFormatException,
    NotFoundException,
)


class StoryNotFound(NotFoundException):
    pass


class StoryExistsException(ExistsException):
    pass


class StoryIncorrectFormatException(IncorrectFormatException):
    pass
