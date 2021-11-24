from app.core.exceptions import (
    ExistsException,
    IncorrectFormatException,
    NotFoundException,
)


class StoryNotFoundException(NotFoundException):
    pass


class StoryExistsException(ExistsException):
    pass


class StoryIncorrectFormatException(IncorrectFormatException):
    pass
