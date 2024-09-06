from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from models.posts import Post
from models.engine.file_storage import FileStorage

app = FastAPI()

file_storage = FileStorage()
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/posts/")
async def create_post(post: Post):
    file_storage.new(post)
    file_storage.save()
    return {"title": post.title, "content": post.content}
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
