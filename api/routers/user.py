from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import get_db
from api.models.user import User
from api.crud.user import create_user, get_user_by_email, get_user_by_id
from schemas.user import UserCreate, ShowUser

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(email=user.email, db=db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(request=user, db=db)

@router.get("/{user_id}", response_model=ShowUser)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(user_id=user_id, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user