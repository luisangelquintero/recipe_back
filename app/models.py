
from typing import Optional
from pydantic import BaseModel


class Recipe(BaseModel):
    title: str
    ingredients: str
    instructions: str
    difficulty: str
    minutes: int

