from app.core.exceptions import ExistsException, NotFoundException


class QuestionNotFound(NotFoundException):
    pass


class QuestionExistsException(ExistsException):
    pass
