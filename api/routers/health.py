from api.database import mongo_db
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    return mongo_db.server_info()
