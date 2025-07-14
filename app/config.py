from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

FAKE_GCS_DIR = BASE_DIR/"fake_gcs"
UPLOAD_DIR = FAKE_GCS_DIR/"uploads"
IMAGE_DB = UPLOAD_DIR/"image_meta.json"

UPLOAD_DIR_STR = str(UPLOAD_DIR)
IMAGE_DB_STR = str(IMAGE_DB)

