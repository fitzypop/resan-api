from functools import lru_cache
from typing import Any

from pydantic import BaseSettings, validator


class _APISettings:
    """A proxy wrapper around a pydantic Settings object.

    Use the function below to get an instance of this class.

    I couldn't figure out pydantics dynamic field types,
    so I made a wrapper with the attrs I need.

    """

    class Settings(BaseSettings):
        db_conn_str = ""
        db_username = ""
        db_password = ""
        app_env = ""
        debug = False

        class Config:
            env_file = ".env"

        @validator("*")
        def must_have_value(cls, v):
            if v in [None, ""]:
                raise ValueError("Env variables not loaded.")
            return v

    def __init__(self) -> None:
        self._settings = self.Settings()
        self.db_conn_str = self._settings.db_conn_str.format(
            self._settings.db_username, self._settings.db_password
        )
        self.db_name = f"Resan{self._settings.app_env}"

    def __getattr__(self, item) -> Any:
        return getattr(self._settings, item)


# Replaced Singleton pattern with lru_cache
@lru_cache
def get_settings() -> _APISettings:
    return api_settings


api_settings = _APISettings()
