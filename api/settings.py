from pydantic import BaseSettings, validator


# No need to import and instantiate this class
# Use settings object below
class _Settings(BaseSettings):
    mongo_conn_str: str = ""
    app_env = ""

    @validator("*")
    def must_have_value(cls, v):
        if v in [None, ""]:
            raise ValueError("Env variables not loaded.")
        return v

    @property
    def db(self):
        return f"Resan{self.app_env}"

    class Config:
        env_file = ".env"


settings = _Settings()
