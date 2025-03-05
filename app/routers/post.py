""" Post route """
from .. import oauth2
from .. import schema
from ..db_storage import get_db
from fastapi import Response, HTTPException, Depends, APIRouter, status
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
import models


# initiate the post route
router = APIRouter(prefix="/posts", tags=["Posts"])

# CRUD operations for posts

# Get all posts
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schema.PostVote])
async def get_posts(db: Session = Depends(get_db),
                    current_user: models.User = Depends(oauth2.get_current_user)
                    , limit: int = 1, offset: int = 0, search: Optional[str] = ''):
    """Get all posts
    Args:
        db: (Session) the database session
        current_user: (User) the current authorized user
        limit: (int) the number of posts to return
        offset: (int) the number of posts to skip
        search: (Optional[str]) searched post by regex pattern
    Returns:
        (List[Dict[str, PostVote]]): voted posts
    """
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(
        models.Vote, models.Vote.post_id == models.Post.id).group_by(
        models.Post.id).filter(
        models.Post.title.contains(
            search)).limit(
        limit).offset(
        offset).all()
    # print(result)
    sterilized_posts = [
        {
            "post": post,
            "votes": votes
        }
        for post, votes in result
    ]
    return sterilized_posts
# Get by a post by id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schema.PostVote)
async def get_post(id: int, db: Session = Depends(get_db),
                   current_user: models.User = Depends(oauth2.get_current_user)):
    """ Get a post by id
    Args:
        id: (int) user's id
        db: (Session) the database session
        current_user: (User) the current authorized user
    Returns:
        Dict[str, PostVote]: voted post
    Raises:
        HTTPException: when no post is found
    """
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(
        models.Vote, models.Vote.post_id == models.Post.id).group_by(
            models.Post.id).filter(models.Post.id == id).first()
    # print(post)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"post": post[0], "votes": post[1]}

# Create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
async def create_post(post: schema.PostCreate, db: Session = Depends(get_db),
                      current_user: models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.model_dump(), user_id=current_user.id)
    if new_post.published is None:
        raise HTTPException(status_code=400, detail="something went wrong")
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schema.Post)
async def get_post(id: int, db: Session = Depends(get_db),
                   current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schema.Post)
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

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=schema.Post)
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
    return Response(status_code=status.HTTP_204_NO_CONTENT)

