from fastapi import FastAPI
from routes import recipe_router
from fake_gcs.routes.images import storage_router


app = FastAPI()
app.include_router(recipe_router)

app.include_router(storage_router)