from datetime import datetime, timedelta
from typing import Awaitable, Callable

from api.database import get_user, update_user_password
from api.models import User, UserJSON
from api.security.exceptions import CREDENTIALS_EXCEPTION
from api.security.hash import needs_rehash, verify_password
from api.settings import API_CONFIG
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr

ALGORITHN = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_user(
    user_generator: Callable[[EmailStr], Awaitable[User]], user_in: UserJSON
) -> User:
    user = await user_generator(user_in.email)

    if not user:
        raise CREDENTIALS_EXCEPTION
    if not verify_password(user.password, user_in.password):
        raise CREDENTIALS_EXCEPTION

    if needs_rehash(user.password):
        await update_user_password(user)

    return user


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, API_CONFIG.SECRET_KEY, algorithm=ALGORITHN)
    return encoded_jwt


async def get_current_active_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, API_CONFIG.SECRET_KEY, algorithms=ALGORITHN)
        username = payload.get("sub")
        if username is None:
            raise CREDENTIALS_EXCEPTION
        token_data = TokenData(username=username)
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    user = await get_user(EmailStr(token_data.username))
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user
