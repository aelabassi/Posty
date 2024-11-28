from fastapi import FastAPI
import os
from dotenv import load_dotenv
from . import db_storage
from app.db_storage import engine
from .routers import user, post, auth


db_storage.Base.metadata.create_all(bind=engine)
load_dotenv()

app = FastAPI()

# include post router
app.include_router(user.router)

# include user router
app.include_router(post.router)

# include auth router
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
