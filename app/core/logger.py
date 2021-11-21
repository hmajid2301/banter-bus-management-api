import logging

import structlog
from structlog.stdlib import BoundLogger


def get_struct_logger(log_level: str) -> BoundLogger:
    logging.getLogger(__name__).setLevel(log_level)
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )

    log = structlog.get_logger()
    return log
