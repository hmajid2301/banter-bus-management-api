from app.core.exceptions import ExistsException, InvalidFilter, NotFoundException


class GameNotFoundException(NotFoundException):
    pass


class GameExistsException(ExistsException):
    pass


class InvalidGameFilter(InvalidFilter):
    pass
