from typing import Optional, List
from functools import lru_cache
from pydantic import BaseSettings
from staging_level import get_environment_file


ENVIRONMENT_FILE = get_environment_file()


class Settings(BaseSettings):
    todos_route: str = "/todos"
    todos_tag: str = "Todos"

    default_limit: int = 10
    default_offset: int = 0

    cors_enabled: Optional[bool] = False
    cors_allow_origins: Optional[List[str]]
    cors_allow_methods: Optional[List[str]]
    cors_allow_headers: Optional[List[str]]

    class Config:
        env_file = ENVIRONMENT_FILE


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
