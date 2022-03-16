from typing import Any

from api.models.base import ExerciseBase
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


class Exercise(ExerciseBase, MongoBaseModel):
    id: MongoObjectId = Field(default_factory=MongoObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True


class User(MongoBaseModel):
    user_id: MongoObjectId = Field(default_factory=MongoObjectId, alias="_id")
    email: EmailStr
    username: str | None = None
    password: str
