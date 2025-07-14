from fastapi import FastAPI
from app.routers.recipes import recipe_router
from app.routers.images import storage_router


app = FastAPI()
app.include_router(recipe_router)
app.include_router(storage_router)