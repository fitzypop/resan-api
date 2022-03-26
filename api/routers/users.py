from api.database import create_user, get_user, update_user_password
from api.models import UserJSON
from api.security.hash import hash_password, needs_rehash, verify_password
from fastapi import APIRouter, HTTPException, status

router = APIRouter(tags=["users"])


@router.get("/user")
def idk_yet():
    return {"hello": "user"}


@router.post("/signup")
async def sign_up_post(new_user: UserJSON):
    try:
        hash = hash_password(new_user.password)
        if not verify_password(hash, new_user.password):
            raise RuntimeError("Error hashing password")

        user = await create_user(new_user, hash)
        return user
    except RuntimeError as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, e.args[0])
    except Exception:
        raise HTTPException(500, "Something went wrong, creating a new user")


@router.post("/signin")
async def sign_in_post(user_in: UserJSON):
    try:
        user = await get_user(user_in)
    except Exception:
        sign_in_error()

    if not verify_password(user.password, user_in.password):
        raise Exception

    if needs_rehash(user.password):
        await update_user_password(user)

    return user


def sign_in_error():
    raise HTTPException(404)  # TODO: fix this later
