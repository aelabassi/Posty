""" User route """
from .. import schema, utils
from ..db_storage import get_db
from fastapi import Response, HTTPException, Depends, APIRouter
from typing import List
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT
from sqlalchemy.orm import Session
import models

# initiate the user route
router = APIRouter(prefix="/users", tags=["Users"])


# CRUD operations for users

# Get all users
@router.get("/", status_code=HTTP_200_OK, response_model=List[schema.UserOut])
async def get_users(db: Session = Depends(get_db)):
    """Get all users
    Args:
        db: (Session) the database session
    Returns:
        users: (List[UserOut]) all users in the database
    """
    users = db.query(models.User).all()
    return users

# Get a user by id
@router.get("/{id}", status_code=HTTP_200_OK, response_model=schema.UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    """ Get a user by id
    Args:
        id: (int) user's id
        db: (Session) the database session
    Returns:
        user (UserOut) the filtered user by id
    """
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Create a new user
@router.post("/", status_code=HTTP_201_CREATED, response_model=schema.UserOut)
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    """Create a user
    Args:
        user (schema.UserCreate): user data to send
        db: (Session) the database session
    Returns:
        new_user: (UserOut) created user information
    """
    # hash the password
    user.password = utils.Hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Update a user
@router.put("/{id}", status_code=HTTP_200_OK, response_model=schema.UserOut)
async def update_user(id: int, updated_user: schema.UserCreate, db: Session = Depends(get_db)):
    """Update user details
    Args:
        id: (int) user's id
        updated_user (UserCreate): user data to update
        db: (Session) the database session
    Returns:
        new_user: (UserOut) updated user information
    Raises:
        HTTPException: if not user is found
    """
    new_user = db.query(models.User).filter(models.User.id == id)
    user = new_user.first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    new_user.update(updated_user.model_dump(), synchronize_session=False)
    db.commit()
    return new_user.first()

# Delete a user
@router.delete("/{id}", status_code=HTTP_200_OK, response_model=schema.UserOut)
async def delete_user(id: int, db: Session = Depends(get_db)):
    """Delete a user form the database
    Args:
        id: (int) user's id'
        db: (Session) the database session
    Returns:
        (Response): 204 status code
    Raises:
        HTTPException: if no user is found
    """
    user = db.query(models.User).filter(models.User.id == id)
    if user.first() is None:
        raise HTTPException(status_code=404, detail=f"User with {id} not found")
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
