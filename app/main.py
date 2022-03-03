import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pymongo import MongoClient
from starlette.responses import RedirectResponse

load_dotenv()

mongo_user = os.environ.get("MONGO_USER")
mongo_password = os.environ.get("MONGO_PASSWORD")
mongo_host = os.environ.get("MONGO_HOST")
conn_str = f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_host}/Exercise?retryWrites=true&w=majority"
client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)
DB = "Exercise"
Collection = "Exercises"

app = FastAPI()


@app.get("/")
def user():
    return RedirectResponse("/docs")


@app.get("/collections")
def get_collections():
    return {"collections": client[DB].list_collection_names()}


@app.get("/exercises")
def get_exercises():
    return client[DB][Collection].find({})
