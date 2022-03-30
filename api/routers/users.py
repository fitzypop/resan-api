from api.database import create_user, get_all_users, get_user
from api.models import User, UserJSON
from api.security import (
    CREDENTIALS_EXCEPTION,
    Token,
    TokenData,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    hash_password,
)
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

router = APIRouter(tags=["users"])


@router.post("/login", response_model=Token)
async def login_for_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(
        get_user,
        UserJSON(email=EmailStr(form_data.username), password=form_data.password),
    )
    if not user:
        raise CREDENTIALS_EXCEPTION
    access_token = create_access_token(
        TokenData(username=user.username, scopes=form_data.scopes)
    )
    return access_token.dict()


@router.post("/signup", response_model=Token)
async def sign_up_post(new_user: UserJSON):
    try:
        hash = hash_password(new_user.password)
        user = await create_user(new_user, hash)
    except RuntimeError as e:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, e.args[0])
    except Exception:
        raise HTTPException(500, "Something went wrong, creating a new user")

    token = create_access_token(TokenData(username=user.username, scopes=user.scopes))
    return token.dict()


@router.get("/users", response_model=list[User])
async def get_users():
    return await get_all_users()


@router.get("/users/me", response_model=User)
async def read_users_me(
    current_user: User = Security(get_current_active_user, scopes=["user:standard"])
):
    return current_user


@router.post("/update/password")
async def update_password(
    user_in: UserJSON,
    current_user: User = Security(get_current_active_user, scopes=["user:standard"]),
):
    new_hash = hash_password(user_in.password)
    return {"current_hash": current_user.hashed_password, "new hash": new_hash}
