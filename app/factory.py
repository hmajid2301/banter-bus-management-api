from structlog.stdlib import BoundLogger

from app.core.config import get_settings
from app.core.logger import get_struct_logger


def get_logger() -> BoundLogger:
    config = get_settings()
    log = get_struct_logger(config.LOG_LEVEL)
    return log
