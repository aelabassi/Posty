from fastapi import FastAPI, Response, status, HTTPException, Depends
import os
from typing import List
from dotenv import load_dotenv
from . import utils

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



HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")




@app.get("/")
async def root():
    return {"message": "Hello World"}

# path operations for posts

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


# path operations for users

# Get all users
@app.get("/users", status_code=HTTP_200_OK, response_model=List[schema.User])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# Get a user by id
@app.get("/users/{id}", status_code=HTTP_200_OK, response_model=schema.User)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Create a new user
@app.post("/users", status_code=HTTP_201_CREATED, response_model=schema.User)
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    # hash the password
    user.password = utils.Hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Update a user
@app.put("/users/{id}", status_code=HTTP_200_OK, response_model=schema.User)
async def update_user(id: int, updated_user: schema.UserCreate, db: Session = Depends(get_db)):
    new_user = db.query(models.User).filter(models.User.id == id)
    user = new_user.first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    new_user.update(updated_user.model_dump(), synchronize_session=False)
    db.commit()
    return new_user.first()

# Delete a user
@app.delete("/users/{id}", status_code=HTTP_200_OK, response_model=schema.User)
async def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if user.first() is None:
        raise HTTPException(status_code=404, detail=f"User with {id} not found")
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


