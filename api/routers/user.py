from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import get_db
from api.models.user import User
from api.crud.user import create_user, get_user_by_email
from schemas.user import UserCreate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(email=user.email, db=db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(request=user, db=db)