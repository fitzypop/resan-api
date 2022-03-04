import os

import motor.motor_asyncio
from dotenv import load_dotenv

from api.model import Exercise

load_dotenv()

_CONN_STR = os.environ.get("MONGO_CONN_STR")
_ENV = os.environ.get("APP_ENV")
_DB = f"Resan{_ENV}"

client = motor.motor_asyncio.AsyncIOMotorClient(_CONN_STR)
database = client[_DB]
collection = database["Exercises"]


async def list_collections() -> list[str]:
    return await database.list_collection_names()


async def fetch_all_exercises() -> list[Exercise]:
    exercises = []
    cursor = collection.find({})
    async for doc in cursor:
        exercises.append(Exercise(**doc))
    return exercises


def get_app_env() -> str:
    return _ENV or ""
