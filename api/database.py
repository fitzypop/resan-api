import motor.motor_asyncio

from api.models import Exercise, ExerciseIn
from api.settings import api_settings

client = motor.motor_asyncio.AsyncIOMotorClient(api_settings.db_conn_str)
mongo_db = client[api_settings.db_name]
collection = mongo_db["Exercises"]


# async def list_collections() -> list[str]:
#     return await mongo_db.list_collection_names()


async def fetch_exercise(name: str) -> Exercise | None:
    return await collection.find_one({"name": name})


async def fetch_all_exercises() -> list[Exercise]:
    exercises = []
    cursor = collection.find({})
    async for doc in cursor:
        exercises.append(Exercise(**doc))
    return exercises


async def create_exercise(exercise: ExerciseIn) -> Exercise:
    doc = exercise.dict()

    found_doc = await collection.find_one(doc)
    if found_doc:
        return Exercise(**found_doc)

    result = await collection.insert_one(doc)
    if not result:
        raise RuntimeError("An error occured inserting a new exercise into the db.")
    return Exercise(**doc)


async def update_exercise(name: str, type: str) -> Exercise:
    await collection.update_one({"name": name}, {"$set": {"type": type}})
    return await collection.find_one({"name": name})


async def delete_exercise(name: str) -> bool:
    await collection.delete_one({"name": name})
    return True


async def health_check():
    return await client.server_info()
