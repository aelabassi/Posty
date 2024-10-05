from pydantic import BaseModel
from typing import Optional

class PostBase(BaseModel):
    """ Base class for Post """
    title: str
    content: str
    published: Optional[bool] = False

    class Config:
        from_attributes = True



class PostCreate(PostBase):
    pass