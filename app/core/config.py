from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "production"
    LOG_LEVEL: str = "DEBUG"

    DB_SCHEMA: str = "mongodb"
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: Optional[int]
    DB_NAME: str
    AUTH_DB_NAME: Optional[str]

    WEB_HOST: str = "0.0.0.0"
    WEB_PORT: int = 8080

    AUTH0_DOMAIN: str
    AUTH0_CUSTOM_API: str

    class Config:
        env_prefix = "BANTER_BUS_MANAGEMENT_API_"
        env_file = ".env"

    def get_mongodb_uri(self) -> str:
        uri = f"{self.DB_SCHEMA}://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}"
        if self.DB_PORT:
            uri += f":{self.DB_PORT}"
        if self.AUTH_DB_NAME:
            uri += f"?authSource={self.AUTH_DB_NAME}"

        return uri


@lru_cache()
def get_settings():
    return Settings()
