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
    _id: MongoObjectId = Field(default_factory=MongoObjectId)
    email: EmailStr = Field(...)
    disabled: bool | None = None
    hashed_password: str = Field(...)
    scopes: list[str] = Field(default_factory=list)

    @property
    def user_id(self) -> ObjectId:
        return self._id

    @property
    def username(self) -> EmailStr:
        """Returns a user's email as username.

        Because I am using OAuth2 Password grant type,
        the BearerToken generator expects a 'username.' But the
        actual OAuth2 specs doesn't care what the username string actually is.

        Returns:
            EmailStr: User's Email as Username
        """
        return self.email

    @username.setter
    def username(self, v: str) -> None:
        self.email = EmailStr(v)

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
