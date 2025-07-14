import json

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import FileResponse
from uuid import uuid4
import re
import os
from datetime import datetime

storage_router = APIRouter()
UPLOAD_DIR = "./fake_gcs/uploads"
IMAGE_DB = "./fake_gcs/uploads/image_meta.json"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def sanitize_filename(text: str) -> str:
    text = text.lower().replace(" ", "-")
    return re.sub(r"[^a-z0-9\-]", "", text)


def save_image_meta(filename: str, recipe_title:str):
    try:
        with open(IMAGE_DB, 'r') as f:
            db = json.load(f)
    except FileNotFoundError:
        db = {}

    db[filename] = {
        "title": recipe_title,
        "temporary": True,
        "timestamp": datetime.utcnow().isoformat()
    }

    with open(IMAGE_DB, 'w') as f:
        json.dump(db, f, indent=2)


@storage_router.post("/upload-image")
async def upload_image(file: UploadFile = File(...), recipe_title: str = Form(...)):
    safe_title = sanitize_filename(recipe_title)
    unique_filename = f"{safe_title}_{uuid4().hex}.jpg"
    file_location = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_location, "wb") as f:
        f.write(await file.read())
    save_image_meta(filename=unique_filename, recipe_title=recipe_title)
    return {"filename:": file.filename, "url": f"/images/{unique_filename}"}


@storage_router.get("/images/{filename}")
async def get_image(filename: str):
    return FileResponse(f"{UPLOAD_DIR}/{filename}")