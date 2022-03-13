from enum import Enum
from typing import Any

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field


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


class MongoBaseModel(BaseModel):
    class Config:
        json_encoders = {ObjectId: str}


class ExerciseType(str, Enum):
    RESISTANCE = "Resistance"
    BODY_WEIGHT = "Body Weight"
    CIRCUIT = "Circuit"
    CARDIO = "Cardio"
    OTHER = "Other"


class ExerciseBase(BaseModel):
    name: str
    type: ExerciseType


class ExerciseIn(ExerciseBase):
    """Use this class for the Body type"""

    pass


class Exercise(ExerciseBase, MongoBaseModel):
    id: MongoObjectId = Field(default_factory=MongoObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True


# TODO: What kind of relationship should user and userprofiles have?
class User(MongoBaseModel):
    user_id: MongoObjectId = Field(default_factory=MongoObjectId, alias="_id")
    email: EmailStr
    password: str


class UserProfile(MongoBaseModel):
    user_id: MongoObjectId
