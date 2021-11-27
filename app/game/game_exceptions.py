from app.core.exceptions import ExistsException, InvalidFilter, NotFoundException


class GameNotFound(NotFoundException):
    pass


class GameExists(ExistsException):
    pass


class InvalidGameFilter(InvalidFilter):
    pass


class GameNotEnabledError(Exception):
    pass
