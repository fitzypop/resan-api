import motor.motor_asyncio

from api.models import Exercise, ExerciseInDb
from api.settings import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_conn_str)
mongo_db = client[settings.db]
collection = mongo_db["Exercises"]


# async def list_collections() -> list[str]:
#     return await mongo_db.list_collection_names()


async def fetch_exercise(name: str) -> Exercise | None:
    return await collection.find_one({"name": name})


async def fetch_all_exercises() -> list[ExerciseInDb]:
    exercises = []
    cursor = collection.find({})
    async for doc in cursor:
        exercises.append(ExerciseInDb(**doc))
    return exercises


async def create_exercise(exercise: Exercise) -> ExerciseInDb:
    doc = exercise.dict()

    found_doc = await collection.find_one(doc)
    if found_doc:
        return ExerciseInDb(**found_doc)

    result = await collection.insert_one(doc)
    if not result:
        raise RuntimeError("An error occured inserting a new exercise into the db.")
    return ExerciseInDb(**doc)


async def update_exercise(name: str, type: str) -> Exercise:
    await collection.update_one({"name": name}, {"$set": {"type": type}})
    return await collection.find_one({"name": name})


async def delete_exercise(name: str) -> bool:
    await collection.delete_one({"name": name})
    return True
