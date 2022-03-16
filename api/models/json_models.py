from api.models.db_models import ExerciseBase
from pydantic import BaseModel, EmailStr, Field, validator


class ExerciseIn(ExerciseBase):
    """Use this class for the Body type"""

    pass


class NewUser(BaseModel):
    email: EmailStr = Field(..., example="some_email@gmail.com")
    username: str | None = Field(..., example="fitzy")
    password: str = Field(..., example="Abc12345?Edf")

    @validator("password")
    def valid_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return v
