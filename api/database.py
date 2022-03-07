import motor.motor_asyncio

from api.model import Exercise
from api.settings import Settings

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
