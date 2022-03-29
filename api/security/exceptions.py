from fastapi import HTTPException, status

CREDENTIALS_EXCEPTION = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
