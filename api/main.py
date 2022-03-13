from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse

from api.database import (
    create_exercise,
    fetch_all_exercises,
    fetch_exercise,
    get_app_env,
    list_collections,
)
from api.models import Exercise, ExerciseInDb
from api.routers import health

app = FastAPI()

app.include_router(health.router)

# use devtools.debug() instead of print()


@app.get("/", include_in_schema=False)
def read_root():
    """Redirect root access to swagger docs."""
    return RedirectResponse("/docs")


@app.get("/collections", response_model=list[str])
async def get_collections():
    response = await list_collections()
    if response:
        return response
    else:
        raise HTTPException(404, "There are no collections in this database")


@app.get("/exercise/{name}", response_model=ExerciseInDb)
async def get_exercise(name: str):
    response = await fetch_exercise(name)
    return response


@app.get("/exercises", response_model=list[ExerciseInDb])
async def get_exercises():
    response = await fetch_all_exercises()
    if response:
        return response
    else:
        raise HTTPException(404, "data not found")


@app.post("/exercise", response_model=ExerciseInDb, status_code=201)
async def post_exercise(exercise: Exercise):
    try:
        response = await create_exercise(exercise)
    except RuntimeError as e:
        raise HTTPException(500, detail=e.args[0])

    return response.dict()


@app.get("/env", response_model=dict[str, str])
def get_env():
    env = get_app_env()
    return {"app_env": env}
