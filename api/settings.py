import copy
from typing import Any

from immute import Immutable
from pydantic import BaseSettings, validator


class _APIConfig(Immutable):
    """A proxy wrapper around a pydantic Settings object.

    Use the function below to get an instance of this class.

    I couldn't figure out pydantics dynamic field types,
    so I made a wrapper with the attrs I need.

    """

    class EnvSettings(BaseSettings):
        db_conn_str = ""
        db_username = ""
        db_password = ""
        app_env: str = "Local"  # available envs: Local, Stage, Prod
        debug = False
        secret_key: str = ""

        class Config:
            env_file = ".env"

        @validator("*", always=True)
        def must_have_value(cls, v):
            if isinstance(v, bool):
                return v
            elif not v:
                raise ValueError("Env variables not loaded.")
            return v

    def __init__(self) -> None:
        _settings = self.EnvSettings()
        for k, v in _settings.dict().items():
            self.__dict__[k] = copy.deepcopy(v)

        self.mongo_conn_str = self.db_conn_str.format(
            self.db_username, self.db_password
        )
        self.db_name = f"Resan{self.app_env}"
        self.title = "Resan API"
        if self.app_env != "Prod":
            self.title = f"{self.app_env} - {self.title}"

    def __getattr__(self, attr: Any) -> Any:
        return getattr(self.__dict__, attr)


API_CONFIG = _APIConfig()
