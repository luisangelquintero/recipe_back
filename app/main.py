from fastapi import FastAPI
from routes import recipe_router
from tinydb import TinyDB


app = FastAPI()

db = TinyDB('test_db.json')


@app.get("/")
def read_root():
    return db.all()
