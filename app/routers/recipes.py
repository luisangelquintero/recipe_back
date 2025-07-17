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

            if not meta[image_name]["title"]:

                image_name_with_title = f'{sanitize_filename(recipe.title)}{image_name}'
                meta[image_name_with_title] = meta.pop(image_name)
                meta[image_name_with_title]["title"] = recipe.title
                os.rename(f"{UPLOAD_DIR}/{image_name}", f"{UPLOAD_DIR}/{image_name_with_title}")

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
