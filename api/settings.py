from pydantic import BaseSettings, validator

# DO NOT IMPORT FROM HERE
# There is a global apisettings object in api/__init__.py/
# Please import as `from api import api_settings`


cla ss APISettings:
    """I couldn't figure out how to dynamically add fields to a `BaseSettings` model.
    So, I made a wrapper around it to add aditional field during `__init__()`."""

    _instance = None

    class Settings(BaseSettings):
        mongo_conn_str: str = ""
        mongo_username: str = ""
        mongo_password: str = ""
        app_env = ""

        class Config:
            env_file = ".env"

        @validator("*")
        def must_have_value(cls, v):
            if v in [None, ""]:
                raise ValueError("Env variables not loaded.")
            return v

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(APISettings, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._settings = self.Settings()
        self.db_conn_str = self._settings.mongo_conn_str.format(
            self._settings.mongo_username, self._settings.mongo_password
        )
        self.db_name = f"Resan{self._settings.app_env}"


api_settings = APISettings()
