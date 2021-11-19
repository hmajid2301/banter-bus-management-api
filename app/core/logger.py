import logging

import structlog
from structlog.stdlib import BoundLogger


class Log:
    def __init__(self) -> None:
        structlog.configure(
            processors=[
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.set_exc_info,
                structlog.processors.TimeStamper(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=False,
        )
        self.log: BoundLogger = structlog.get_logger()

    def update_log_level(self, log_level: str):
        level = logging.getLevelName(log_level)
        self.log.setLevel(level)
