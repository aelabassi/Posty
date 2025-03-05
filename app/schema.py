from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime
import models


# Posts
class PostBase(BaseModel):
    """ Base class for Post"""
    title: str
    content: str
    published: Optional[bool] = False


# Users

class UserBase(BaseModel):
    """ Base class for User """
    username: str
    email: EmailStr
    password: str

class UserCreate(UserBase):
    """Response model at login request"""
    email: EmailStr
    password: str

class UserOut(BaseModel):
    "Response model at login response"
    id: int
    username: str
    email: EmailStr
    created_at: Optional[datetime] = datetime.now()

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str


# Posts
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: Optional[datetime] = datetime.now()
    user_id: int
    user: UserOut

    class Config:
        from_attributes = True

# votes
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

    class Config:
        from_attributes = True


class PostVote(BaseModel):
    post: Post
    votes: int

class Token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
