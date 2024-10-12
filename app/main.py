from fastapi import FastAPI, Response, status, HTTPException, Depends
import os
from typing import List
from dotenv import load_dotenv
import time

from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT

import models
from models import Post
from . import schema
import db_storage
from db_storage import engine, session
from sqlalchemy.orm import Session
db_storage.Base.metadata.create_all(bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

load_dotenv()

app = FastAPI()

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data":posts}

HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")




@app.get("/")
async def root():
    return {"message": "Hello World"}

# Get all posts
@app.get("/posts", status_code=HTTP_200_OK, response_model=List[schema.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts
# Get by a post by id
@app.get("/posts/{id}", status_code=HTTP_200_OK, response_model=schema.Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# Create a new post
@app.post("/posts", status_code=HTTP_201_CREATED, response_model=schema.Post)
async def create_post(post: schema.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    if new_post.published is None:
        raise HTTPException(status_code=400, detail="something went wrong")
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", status_code=HTTP_200_OK, response_model=schema.Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.put("/posts/{id}", status_code=HTTP_200_OK, response_model=schema.Post)
async def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db)):
    new_post = db.query(models.Post).filter(models.Post.id == id)
    post = new_post.first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    new_post.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    # db.refresh(new_post)
    return new_post.first()

@app.delete("/posts/{id}", status_code=HTTP_200_OK, response_model=schema.Post)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=404, detail=f"Post with {id} not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)



