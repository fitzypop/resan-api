from fastapi import APIRouter

router = APIRouter(tags=["users"])


@router.get("/user")
def idk_yet():
    return {"hello": "user"}
