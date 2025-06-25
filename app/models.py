
from pydantic import BaseModel


class Recipe(BaseModel):
    id: str
    title: str
    difficulty: str
    ingredients: str
    minutes: int
    instructions: str
    imagePath: str



