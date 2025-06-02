
from pydantic import BaseModel


class Recipe(BaseModel):
    title: str
    ingredients: list[str]
    instructions: str
    difficulty: str
    time: int
    submitted_by: str
    timestamp: str
    id: str
