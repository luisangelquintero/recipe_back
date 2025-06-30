import json
from fastapi import APIRouter
from models import Recipe
from tinydb import TinyDB


recipe_router = APIRouter()

db = TinyDB('test_db.json')
IMAGE_DB = "./uploads/image_meta.json"


@recipe_router.post("/recipes")
def add_recipe(recipe: Recipe):
    db.insert(recipe.model_dump())

    # mark image as permanent
    try:
        with open(IMAGE_DB, 'r') as f:
            meta = json.load(f)
        image_name = recipe.imagePath.split("/")[-1]
        if image_name in meta:
            meta[image_name]["temporary"] = False

        with open(IMAGE_DB, "w") as f:
            json.dump(meta, f, indent=2)
    except Exception as e:
        print(f"⚠️ Couldn't update image metadata: {e}")
    return {"message": "Recipe added!"}


@recipe_router.get("/recipes")
def get_recipes():
    return db.all()


@recipe_router.post("/recipes/deleteAll")
def delete_recipes():
    return db.truncate()
