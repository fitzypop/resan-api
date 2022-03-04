from pydantic import BaseModel


class Exercise(BaseModel):
    name: str
    type: str
