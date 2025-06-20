from fastapi import FastAPI
from routes.images import router as image_router

app = FastAPI()
app.include_router(image_router)