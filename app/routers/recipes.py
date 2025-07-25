import json
import os
from fastapi import APIRouter
from tinydb import TinyDB
from pathlib import Path

from app.utils import sanitize_filename
from app.config import IMAGE_DB, UPLOAD_DIR
from app.models import Recipe


recipe_router = APIRouter()
DATA_PATH = Path(__file__).resolve().parent.parent / "data"
DATA_PATH.mkdir(parents=True, exist_ok=True)
db = TinyDB(DATA_PATH / "recipes_dt.json")


def process_image_data(recipe: Recipe):
    try:
        with open(IMAGE_DB, 'r') as f:
            image_metadata = json.load(f)
        image_name = recipe.imagePath.split("/")[-1]

        if image_name in image_metadata:
            image_metadata[image_name]["temporary"] = False

            if not image_metadata[image_name]["title"]:
                image_name_with_title = f'{sanitize_filename(recipe.title)}{image_name}'
                image_metadata[image_name_with_title] = image_metadata.pop(image_name)
                image_metadata[image_name_with_title]["title"] = recipe.title
                recipe.imagePath = f"/images/{image_name_with_title}"
                os.rename(f"{UPLOAD_DIR}/{image_name}", f"{UPLOAD_DIR}/{image_name_with_title}")

        with open(IMAGE_DB, "w") as f:
            json.dump(image_metadata, f, indent=2)
    except Exception as e:
        print(f"⚠️ Couldn't update image metadata: {e}")


@recipe_router.post("/recipe")
def add_recipe(recipe: Recipe):
    process_image_data(recipe)
    db.insert(recipe.model_dump())
    return {"message": "Recipe added!"}


@recipe_router.get("/recipes")
def get_recipes():
    return db.all()


@recipe_router.post("/recipes/deleteAll")
def delete_recipes():
    return db.truncate()
