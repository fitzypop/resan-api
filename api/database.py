import motor.motor_asyncio
from pydantic import EmailStr

from api.models.db_models import Exercise, User
from api.models.json_models import ExerciseIn
from api.settings import get_settings

settings = get_settings()
client = motor.motor_asyncio.AsyncIOMotorClient(settings.db_conn_str)
mongo_db = client[settings.db_name]
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


def hash_password(password: str) -> str:
    return f"really-bad-hash-{password}"


async def email_already_exists(email: EmailStr) -> bool:
    return await collection.find


async def create_user(new_user):
    # check for unique email
    hashed = hash_password(new_user.password)

    return User(**new_user.dict(), password=hashed)
