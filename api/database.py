import motor.motor_asyncio
from pydantic import EmailStr

from api.models import Exercise, ExerciseIn, User
from api.settings import get_settings

settings = get_settings()
client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_conn_str)
db = client[settings.db_name]
exr_coll = db["exercises"]
users_coll = db["users"]


# async def list_collections() -> list[str]:
#     return await mongo_db.list_collection_names()


# TODO: can I move this setup code to terraform, or other db management/migration thingy?
async def manage_db() -> None:
    await users_coll.create_index("email", unique=True, name="unique_email")
    await exr_coll.create_index("name", unique=True, name="unique_name")


async def fetch_exercise(name: str) -> Exercise | None:
    return await exr_coll.find_one({"name": name.title()})


async def fetch_all_exercises() -> list[Exercise]:
    exercises = []
    cursor = exr_coll.find({})
    async for doc in cursor:
        exercises.append(Exercise(**doc))
    return exercises


async def create_exercise(exercise: ExerciseIn) -> Exercise:
    doc = exercise.dict()

    found_doc = await exr_coll.find_one(doc)
    if found_doc:
        return Exercise(**found_doc)

    result = await exr_coll.insert_one(doc)

    if not result:
        raise RuntimeError("An error occured inserting a new exercise into the db.")
    return Exercise(**doc)


async def update_exercise(name: str, type: str) -> Exercise:
    await exr_coll.update_one({"name": name}, {"$set": {"type": type}})
    return await exr_coll.find_one({"name": name})


async def delete_exercise(name: str) -> bool:
    await exr_coll.delete_one({"name": name})
    return True


async def health_check():
    return await client.server_info()


def hash_password(password: str) -> str:
    return f"really-bad-hash-{password}"


async def email_already_exists(email: EmailStr) -> bool:
    return await exr_coll.find


async def create_user(new_user):
    # check for unique email
    hashed = hash_password(new_user.password)

    return await users_coll.insert_one(User(**new_user.dict(), password=hashed).dict())
