from datetime import datetime, timedelta
from typing import Awaitable, Callable

from argon2 import PasswordHasher
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr, Field

from api.database import get_user, update_user_password
from api.models import User, UserJSON
from api.settings import API_CONFIG

CREDENTIALS_EXCEPTION = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

ALGORITHN = "HS256"
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login", scopes={"user:standard": "Allow access scoped to a Standard User"}
)


async def authenticate_user(
    user_generator: Callable[[EmailStr], Awaitable[User]], user_in: UserJSON
) -> User:
    user = await user_generator(user_in.email)

    if not user:
        raise CREDENTIALS_EXCEPTION
    if not verify_password(user.hashed_password, user_in.password):
        raise CREDENTIALS_EXCEPTION

    if needs_rehash(user.hashed_password):
        await update_user_password(user)

    return user


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = Field(default_factory=list)


def create_access_token(data: TokenData) -> Token:
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode = {"exp": expire, "iat": datetime.utcnow(), "sub": data.username}
    encoded_jwt = jwt.encode(to_encode, API_CONFIG.secret_key, algorithm=ALGORITHN)
    return Token(access_token=encoded_jwt)


async def get_current_active_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, API_CONFIG.secret_key, algorithms=ALGORITHN)
        username = payload.get("sub")
        if username is None:
            raise CREDENTIALS_EXCEPTION
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(username=username, scopes=token_scopes)
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    user = await get_user(EmailStr(token_data.username))
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user


ph = PasswordHasher()


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(hash, password) -> bool:
    return ph.verify(hash, password)


def needs_rehash(hash) -> bool:
    return ph.check_needs_rehash(hash)
