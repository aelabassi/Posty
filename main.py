from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from models.posts import Post
from models.engine.file_storage import FileStorage
import uuid

app = FastAPI()

file_storage = FileStorage()

def find_post(id):
    file_storage.reload()
    for post in file_storage.all(Post).values():
        if post.id == id:
            return post
    return None
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts/")
async def get_posts():
    file_storage.reload()
    file_storage.all(Post)
    return {"data": file_storage.all(Post)}
@app.post("/posts/")
async def create_post(post: Post):
    file_storage.new(post)
    file_storage.save()
    return {"id": post.id ,"title": post.title, "content": post.content}

@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    post = find_post(post_id)
    return {"data": post}
