from enum import Enum
from typing import Any

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, validator

""" Base Objects """


class MongoObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None:
        field_schema.update(
            type="string",
        )

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not isinstance(v, (ObjectId, cls)) or not ObjectId.is_valid(v):
            raise TypeError("invalid ObjectId specified")
        return v


class ExerciseType(str, Enum):
    RESISTANCE = "Resistance"
    BODY_WEIGHT = "Body Weight"
    CIRCUIT = "Circuit"
    CARDIO = "Cardio"
    OTHER = "Other"


""" JSON Models"""


class ExerciseJSON(BaseModel):
    name: str
    type: ExerciseType

    @validator("name")
    def name_title(cls, v) -> str:
        if not v:
            raise ValueError("Must have a name")
        return v.title()


class UserJSON(BaseModel):
    email: EmailStr = Field(..., example="some_email@gmail.com")
    password: str = Field(..., example="Abc12345?Edf")

    @validator("password")
    def valid_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return v


# TODO: need to validate email string
# TODO: email validation setup? i.e. "We sent an email to your email to verify" then redirect?

""" DB Models"""


class Exercise(ExerciseJSON):
    id: MongoObjectId = Field(default_factory=MongoObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True


class User(BaseModel):
    id: MongoObjectId = Field(default_factory=MongoObjectId, alias="_id")
    email: str = Field(...)
    password: str = Field(...)
    username: str | None = None
    disabled: bool | None = None

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
