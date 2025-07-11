import json
from fastapi import APIRouter
from models import Recipe
from tinydb import TinyDB
from fake_gcs.routes.images import sanitize_filename, UPLOAD_DIR
import os


recipe_router = APIRouter()

db = TinyDB('test_db.json')
IMAGE_DB = "./fake_gcs/uploads/image_meta.json"


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
