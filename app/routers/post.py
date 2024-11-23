from .. import oauth2
from .. import schema
from ..db_storage import get_db
from fastapi import Response, HTTPException, Depends, APIRouter
from typing import List
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT
from sqlalchemy.orm import Session
import models



router = APIRouter(prefix="/posts", tags=["Posts"])

# CRUD operations for posts

# Get all posts
@router.get("/", status_code=HTTP_200_OK, response_model=List[schema.Post])
async def get_posts(db: Session = Depends(get_db),
                    current_user: models.User = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    return posts
# Get by a post by id
@router.get("/{id}", status_code=HTTP_200_OK, response_model=schema.Post)
async def get_post(id: int, db: Session = Depends(get_db),
                   current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# Create a new post
@router.post("/", status_code=HTTP_201_CREATED, response_model=schema.Post)
async def create_post(post: schema.PostCreate, db: Session = Depends(get_db),
                      current_user: models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.model_dump(), user_id=current_user.id)
    if new_post.published is None:
        raise HTTPException(status_code=400, detail="something went wrong")
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", status_code=HTTP_200_OK, response_model=schema.Post)
async def get_post(id: int, db: Session = Depends(get_db),
                   current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{id}", status_code=HTTP_200_OK, response_model=schema.Post)
async def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db),
                      current_user: models.User = Depends(oauth2.get_current_user)):
    new_post = db.query(models.Post).filter(models.Post.id == id)
    post = new_post.first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    # only the owner of the post can update it
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to update this post")

    new_post.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    # db.refresh(new_post)
    return new_post.first()

@router.delete("/{id}", status_code=HTTP_200_OK, response_model=schema.Post)
async def delete_post(id: int, db: Session = Depends(get_db),
                      current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=404, detail=f"Post with {id} not found")

    # only the owner of the post can delete it
    if post.first().user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this post")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)

