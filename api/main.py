import json
import os

from bson import json_util
from dotenv import load_dotenv
from fastapi import FastAPI
from pymongo import MongoClient
from starlette.responses import RedirectResponse

load_dotenv()

_env = os.environ.get("HEROKU_ENV")
_conn_str = os.environ.get("MONGO_CONN_STR")
_client = MongoClient(_conn_str, serverSelectionTimeoutMS=5000)
_DB = f"Db-{_env}"
_Collection = "Exercises"

app = FastAPI()


@app.get("/", include_in_schema=False)
def user():
    return RedirectResponse("/docs")


@app.get("/collections")
def get_collections():
    return {"collections": _client[_DB].list_collection_names()}


@app.get("/exercises")
def get_exercises():
    cursor = _client[_DB][_Collection].find({})
    return {i: json.loads(json_util.dumps(doc)) for i, doc in enumerate(cursor)}


@app.get("/env")
def get_env():
    return {"heroku_env": _env}
