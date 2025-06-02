
from pydantic import BaseModel


class Recipe(BaseModel):
    title: str
    ingredients: list[str]
    instructions: str
    difficulty: str
    effort: int
    submitted_by: str
    timestamp: str
