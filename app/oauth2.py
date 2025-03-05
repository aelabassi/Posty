"""
Oauth2 Module: Authentication using JWT tokens
"""
from jose import JWSError, jwt
from datetime import datetime, timedelta
from . import schema, db_storage
import models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
oath2_scheme = OAuth2PasswordBearer(tokenUrl="login")
## prerequisites
# Secret key for encoding and decoding JWT tokens
# Algorithm for encoding and decoding JWT tokens
# Token expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRATION_TIME_MINUTE = settings.access_token_expire_minutes


def create_access_token(data: dict):
    """ Create a new access token
     Args:
         data: (dict) data to encode
     Returns:
         (str): JWT string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME_MINUTE)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token:str, credentials_exception: Exception):
    """ Verify the access token
     Args:
         token (str): Access token
         credentials_exception (Exception): Exception to raise
    Returns:
        (TokenData):  the token schema
    Raises:
        credentials_exception: when JWSError
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schema.TokenData(user_id=user_id)
    except JWSError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oath2_scheme), db: Session = Depends(db_storage.get_db)):
    """ Get the current user
    Args:
        token (str): Access token depends on oath2_scheme
        db: the database session depends on get_db
    Returns:
         user (Query | Any): filtered user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.user_id).first()
    if user is None:
        raise credentials_exception
    return user