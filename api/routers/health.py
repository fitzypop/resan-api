import json

from api.database import client
from devtools import debug
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    db_results = await client.server_info()
    debug(db_results)
    return db_results
