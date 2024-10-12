from fastapi import FastAPI
import os
from dotenv import load_dotenv
from . import db_storage
from app.db_storage import engine
from .routers import user, post


db_storage.Base.metadata.create_all(bind=engine)
load_dotenv()

app = FastAPI()



HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")

# include post router
app.include_router(user.router)

# include user router
app.include_router(post.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
