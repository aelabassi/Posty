from fastapi import FastAPI, Response, status, HTTPException
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
@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    file_storage.new(post)
    file_storage.save()
    return {"id": post.id ,"title": post.title, "content": post.content}


@app.get("/posts/latest")
async def get_latest_post():
    file_storage.reload()
    posts = file_storage.all(Post).values()
    latest = max(posts, key=lambda post: post.id)
    return {"data": latest}
@app.get("/posts/{post_id}")
async def get_post(post_id: int, response: Response):
    post = find_post(post_id)
    if post is None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"data": post}

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    post = find_post(post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    file_storage.delete(post)
    file_storage.save()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: Post):
    post = find_post(post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post.title = post.title
    post.content = post.content
    post.published = post.published
    post.rating = post.rating
    file_storage.save()
    return {"data": post}

