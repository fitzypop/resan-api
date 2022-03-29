from api.database import create_user, get_all_users, get_user
from api.models import User, UserJSON
from api.security import (
    Token,
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from api.security.exceptions import CREDENTIALS_EXCEPTION
from api.security.hash import hash_password

# from api.security.hash import verify_password
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

router = APIRouter(tags=["users"])


@router.get("/users", response_model=list[User])
async def get_users():
    return await get_all_users()


@router.post("/token", response_model=Token)
async def login_for_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(
        get_user,
        UserJSON(email=EmailStr(form_data.username), password=form_data.password),
    )
    if not user:
        raise CREDENTIALS_EXCEPTION
    access_token = create_access_token(
        data={"sub": user.email, "scopes": form_data.scopes}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/signup", response_model=User)
async def sign_up_post(new_user: UserJSON):
    try:
        hash = hash_password(new_user.password)
        user = await create_user(new_user, hash)
        return user
    except RuntimeError as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, e.args[0])
    except Exception:
        raise HTTPException(500, "Something went wrong, creating a new user")
