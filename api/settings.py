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

        @validator("db_conn_str", "db_username", "db_password", "app_env", always=True)
        def must_have_value(cls, v):
            if not v:
                raise ValueError("Env variables not loaded.")
            return v

    def __init__(self) -> None:
        self._settings = self.Settings()
        self.mongo_conn_str = self._settings.db_conn_str.format(
            self._settings.db_username, self._settings.db_password
        )
        self.db_name = f"Resan{self._settings.app_env}"

    def __getattr__(self, attr) -> Any:
        _attr = getattr(self._settings, attr)
        if hasattr(type(_attr), "__get__"):  # attr is a method
            _attr = _attr.__get__(
                self._settings
            )  # set _settings as self on method call
        return _attr

    def __delattr__(self, __name: str) -> None:
        raise NotImplementedError(
            f"{_APISettings.__name__} does not support deleting attributes."
        )

    @property
    def title(self) -> str:
        if not hasattr(self, "_title"):
            self._title = "Resan API"
            if self.app_env != "Prod":
                self._title = f"{self.app_env} - {self._title}"
        return self._title


# Replaced Singleton pattern with lru_cache

# Please either import the function or module variable below.
# We don't need multiple instances of these settings.
@lru_cache
def get_settings() -> _APISettings:
    return api_settings


api_settings = _APISettings()
