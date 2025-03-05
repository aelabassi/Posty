from multiprocessing.sharedctypes import synchronized

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..schema import Vote
from ..db_storage import get_db
from ..oauth2 import get_current_user
from typing import Any
import models

# initiate the vote router
router = APIRouter(
    prefix="/vote",
    tags=["Vote"],
    responses={404: {"description": "Not found"}},
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), current_user: Any = Depends(get_current_user)):
    """ Vote on a post
     Args:
         vote: (Vote) the vote model
         db: (Session) the database session depends on get_db
         current_user: (str) the current authorized user
    Returns:
        Dict[str, str]: dictionary contains the message if the post is voted or not
    Raises:
        HTTPException: if no post to vote on or the post is already been voted
        or no vote on the post
    """
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {vote.post_id} not found")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    voted = vote_query.first()
    if vote.dir == 1:
        if voted:
            raise HTTPException(status_code=409,
                                detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote created successfully"}
    else:
        if not voted:
            raise HTTPException(status_code=404,
                                detail=f"User {current_user.id} has not voted on post {vote.post_id}")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted successfully"}