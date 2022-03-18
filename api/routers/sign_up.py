from http.client import HTTPException

from api.database import create_user
from api.models import NewUser
from fastapi import APIRouter, status

router = APIRouter(tags=["Sign Up"])


@router.post("/signup")
async def sign_up_post(new_user: NewUser):
    try:
        user = await create_user(new_user)
        return user
    except RuntimeError as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, e.args[0])
    except Exception:
        raise HTTPException(500, "Something went wrong, creating a new user")
