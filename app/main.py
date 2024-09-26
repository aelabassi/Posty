from fastapi import FastAPI, Response, status, HTTPException, Depends
import os
from dotenv import load_dotenv
import time
import models
from models import Post
import db_storage
from db_storage import engine, session
from sqlalchemy.orm import Session
db_storage.Base.metadata.create_all(engine)

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
@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}
# Get by a post by id
@app.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"data": post}

# Create a new post
@app.post("/posts")
async def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

