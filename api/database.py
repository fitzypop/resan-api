# import os

import motor.motor_asyncio
from pydantic import BaseSettings, validator

from api.model import Exercise

# from dotenv import load_dotenv


# load_dotenv()

_SENTINEL = "_SENTINEL"


class Settings(BaseSettings):
    mongo_conn_str: str = _SENTINEL
    app_env: str = _SENTINEL

    @validator("*")
    def populate_conn_str(cls, v):
        if v in [None, "", _SENTINEL]:
            raise ValueError("Environment variables were not properly loaded")
        return v

    @property
    def db(self):
        return f"Resan{self.app_env}"

    class Config:
        env_file = ".env"


settings = Settings()
client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_conn_str)
database = client[settings.db]
collection = database["Exercises"]


async def list_collections() -> list[str]:
    return await database.list_collection_names()


async def fetch_exercise(name: str) -> Exercise | None:
    return await collection.find_one({"name": name})


async def fetch_all_exercises() -> list[Exercise]:
    exercises = []
    cursor = collection.find({})
    async for doc in cursor:
        exercises.append(Exercise(**doc))
    return exercises


async def create_exercise(exercise: Exercise) -> Exercise:
    result = await collection.insert_one(exercise)
    return exercise


async def update_exercise(name: str, type: str) -> Exercise:
    await collection.update_one({"name": name}, {"$set": {"type": type}})
    return await collection.find_one({"name": name})


async def delete_exercise(name: str) -> bool:
    await collection.delete_one({"name": name})
    return True


def get_app_env() -> str:
    return settings.app_env or ""
