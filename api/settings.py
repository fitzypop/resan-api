from typing import Any

from pydantic import BaseSettings, validator


class _APIConfig:
    """A proxy wrapper around a pydantic Settings object.

    Use the function below to get an instance of this class.

    I couldn't figure out pydantics dynamic field types,
    so I made a wrapper with the attrs I need.

    """

    class Secrets(BaseSettings):
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
        # self.__dict__["_settings"] = self.Secrets()
        secrets = self.Secrets()
        self.__dict__["_secrets"] = secrets
        for k, v in secrets.__dict__.items():
            self.__dict__[k] = v

        self.__dict__["mongo_conn_str"] = self.db_conn_str.format(
            self.db_username, self.db_password
        )
        self.__dict__["db_name"] = f"Resan{self.app_env}"
        title = "Resan API"
        if self.app_env != "Prod":
            title = f"{self.app_env} - {title}"
        self.__dict__["title"] = title

    def __getattr__(self, attr) -> Any:
        _attr = getattr(self._secrets, attr)
        if hasattr(type(_attr), "__get__"):  # attr is a method
            _attr = _attr.__get__(self._secrets)  # set _settings as self on method call
        return _attr

    def __delattr__(self, __name: str) -> None:
        raise NotImplementedError(
            f"{_APIConfig.__name__} does not support deleting attributes."
        )

    def __setattr__(self, __name: str, __value: Any) -> None:
        raise NotImplementedError()


API_CONFIG = _APIConfig()
