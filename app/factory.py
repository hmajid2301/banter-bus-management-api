from typing import List

from fastapi_cloudauth.auth0 import Auth0
from fastapi_cloudauth.base import ScopedAuth
from structlog.stdlib import BoundLogger

from app.core.config import get_settings
from app.core.logger import get_struct_logger


def get_logger() -> BoundLogger:
    config = get_settings()
    log = get_struct_logger(config.LOG_LEVEL)
    return log


def get_auth(scopes: List[str]) -> ScopedAuth:
    config = get_settings()
    auth = Auth0(domain=config.AUTH0_DOMAIN, customAPI=config.AUTH0_CUSTOM_API)
    return auth.scope(scopes)


def get_read_scopes():
    scopes = get_auth(["admin:read"])
    return scopes


def get_write_scopes():
    scopes = get_auth(["admin:write"])
    return scopes
