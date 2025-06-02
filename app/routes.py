from fastapi import APIRouter
from models import Recipe


recipe_router = APIRouter()


@recipe_router.get("/recipes")
def get_recipes():
    return [{"title": "Pizza", "difficulty": "Easy"}]
