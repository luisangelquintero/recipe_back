from fastapi import FastAPI
from routes import recipe_router


app = FastAPI()
app.include_router(recipe_router)
