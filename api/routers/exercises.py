from api.database import create_exercise, fetch_all_exercises, fetch_exercise
from api.models import Exercise, ExerciseInDb
from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["exercise"])


@router.get("/exercise/{name}", response_model=ExerciseInDb)
async def get_exercise(name: str):
    response = await fetch_exercise(name)
    return response


@router.get("/exercises", response_model=list[ExerciseInDb])
async def get_exercises():
    response = await fetch_all_exercises()
    if response:
        return response
    else:
        raise HTTPException(404, "data not found")


@router.post("/exercise", response_model=ExerciseInDb, status_code=201)
async def post_exercise(exercise: Exercise):
    try:
        response = await create_exercise(exercise)
    except RuntimeError as e:
        raise HTTPException(500, detail=e.args[0])

    return response.dict()
