from enum import Enum

from pydantic import BaseModel


class ExerciseType(str, Enum):
    RESISTANCE = "Resistance"
    BODY_WEIGHT = "Body Weight"
    CIRCUIT = "Circuit"
    CARDIO = "Cardio"
    OTHER = "Other"


class ExerciseBase(BaseModel):
    name: str
    type: ExerciseType
