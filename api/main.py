# import json
# import os

# from bson import json_util
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from api.database import fetch_all_exercises, get_app_env, list_collections

app = FastAPI()


@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse("/docs")


@app.get("/collections")
async def get_collections():
    response = await list_collections()
    return {"collections": response}


@app.get("/exercises")
async def get_exercises():
    response = await fetch_all_exercises()
    return response


@app.get("/env")
def get_env():
    env = get_app_env()
    return {"app_env": env}
