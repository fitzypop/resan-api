import json

from api.database import client
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    db_results = await client.server_info()
    return json.dumps(db_results)
