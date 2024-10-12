from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    """ Base class for Post """
    title: str
    content: str
    published: Optional[bool] = False





class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: Optional[datetime] = datetime.now()

    class Config:
        from_attributes = True
