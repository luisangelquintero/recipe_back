from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
import os

storage_router = APIRouter()
UPLOAD_DIR = "./fake_gcs/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@storage_router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"filename:": file.filename, "url": f"/images/{file.filename}"}


@storage_router.get("/images/{filename}")
async def get_image(filename: str):
    return FileResponse(f"{UPLOAD_DIR}/{filename}")