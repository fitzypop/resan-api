from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    mongo_conn_str: str = ""
    app_env = ""

    @validator("*")
    def must_have_value(cls, v):
        if v in [None, ""]:
            raise ValueError("Env variables not loaded.")

    @property
    def db(self):
        return f"Resan{self.app_env}"

    class Config:
        env_file = ".env"
