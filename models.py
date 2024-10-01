from sqlalchemy import Column, Integer, String, DateTime, Boolean, TIMESTAMP, text
from db_storage import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(128), nullable=False)
    content = Column(String(128), nullable=False)
    published = Column(Boolean, default=False, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class PostResponse(BaseModel):
    title: str
    content: str
    published: Optional[bool] = False

    class Config:
        from_attributes = True