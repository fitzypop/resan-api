import os

from dotenv import load_dotenv
from fastapi import FastAPI
from pymongo import MongoClient
from starlette.responses import RedirectResponse

load_dotenv()

_env = os.environ.get("HEROKU_ENV")
_conn_str = os.environ.get("MONGO_CONN_STR")
_client = MongoClient(_conn_str, serverSelectionTimeoutMS=5000)
_DB = "Exercise"
_Collection = "Exercises"

app = FastAPI()


@app.get("/")
def user():
    return RedirectResponse("/docs")


@app.get("/collections")
def get_collections():
    return {"collections": _client[_DB].list_collection_names()}


@app.get("/exercises")
def get_exercises():
    return _client[_DB][_Collection].find({})


@app.get("/env")
def get_env():
    return {"heroku_env": _env}
