from sqlalchemy import (
    Column, Integer, String,
    Boolean, TIMESTAMP, text,
ForeignKey)
from sqlalchemy.orm import relationship
from app.db_storage import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(128), nullable=False)
    content = Column(String(128), nullable=False)
    published = Column(Boolean, default=False, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    user = relationship('User')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(128), nullable=False, unique=True)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)