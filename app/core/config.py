from functools import lru_cache

from omnibus.config.settings import OmnibusSettings


class Settings(OmnibusSettings):
    AUTH0_DOMAIN: str
    AUTH0_CUSTOM_API: str

    class Config:
        env_prefix = "BANTER_BUS_MANAGEMENT_API_"
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
