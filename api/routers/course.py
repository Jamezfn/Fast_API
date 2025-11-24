from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import get_db
from schemas.course import CourseCreate, CourseShow
from api.models.user import User
from api.crud.course import create_course

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

@router.post('/create',response_model=CourseShow, status_code=status.HTTP_201_CREATED)
def create_post(request: CourseCreate, db: Session = Depends(get_db)):
    result = create_course(request, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Course creation failed - course may already exist or teacher not found"
            )
    
    return result