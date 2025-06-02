from fastapi import APIRouter
from models import Recipe
from tinydb import TinyDB


recipe_router = APIRouter()

db = TinyDB('test_db.json')


@recipe_router.post("/recipes")
def add_recipe(recipe: Recipe):
    db.insert(recipe.dict())
    return {"message": "Recipe added!"}


@recipe_router.get("/recipes")
def get_recipes():
    return db.all()
