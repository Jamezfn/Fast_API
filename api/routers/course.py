from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db import get_db
from schemas.course import(
    ContentBlockCreate, ContentBlockResponse, CourseCreate, CourseShow, CourseUpdate, 
    SectionCreate, SectionShow, SectionUpdate, ContentBlockUpdate, )
from api.models.user import User
from api.crud.course import (
    create_course, create_section, get_course, get_course_by_teacher, get_courses,
    update_course, delete_course, get_section, update_section, delete_section,
    create_content_block, get_content_block, update_content_block, delete_content_block, get_all_content_blocks,
    get_content_blocks_by_section_id)

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

@router.get('/all', response_model=List[CourseShow])
def get_all_courses(db: Session = Depends(get_db)):
    result = get_courses(db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Courses not found"
            )
    
    return result

@router.get('/get/{course_id}', response_model=CourseShow)
def get_course_by_id(course_id: int, db: Session = Depends(get_db)):
    result = get_course(course_id, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Course not found"
            )
    
    return result


@router.get('/teacher/{teacher_id}', response_model=List[CourseShow])
def get_courses_by_teacher(teacher_id: int, db: Session = Depends(get_db)):
    result = get_course_by_teacher(teacher_id, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Courses not found"
            )
    
    return result

@router.put('/update/{course_id}', response_model=CourseShow)
def update_course_by_id(course_id: int, request: CourseUpdate, db: Session = Depends(get_db)):
    result = update_course(course_id, request, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Course not found"
            )
    
    return result

@router.delete('/delete/{course_id}', response_model=CourseShow)
def delete_course_by_id(course_id: int, db: Session = Depends(get_db)):
    result = delete_course(course_id, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Course not found"
            )
    
    return result

@router.post('/create/{course_id}/section', response_model=SectionShow)
def create_section_by_course_id(course_id: int, request: SectionCreate, db: Session = Depends(get_db)):
    result = create_section(course_id, request, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Course not found"
            )
    
    return result

@router.get('/section/{section_id}', response_model=SectionShow)
def get_section_by_id(section_id: int, db: Session = Depends(get_db)):
    result = get_section(section_id, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Section not found"
            )
    
    return result

@router.put('/section/{section_id}', response_model=SectionShow)
def update_section_by_id(section_id: int, request: SectionUpdate, db: Session = Depends(get_db)):
    result = update_section(section_id, request, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Section not found"
            )
    
    return result

@router.delete('/section/{section_id}', response_model=SectionShow)
def delete_section_by_id(section_id: int, db: Session = Depends(get_db)):
    result = delete_section(section_id, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Section not found"
            )
    
    return result

@router.get('/section/content/all_content_blocks', response_model=List[ContentBlockResponse])
def get_all_content_blocks_route(db: Session = Depends(get_db)):
    result = get_all_content_blocks(db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No content blocks found"
            )
    
    return result

@router.post('/section/{section_id}/create_content_block', response_model=ContentBlockCreate)
def create_content_block_by_section_id(section_id: int, request: ContentBlockCreate, db: Session = Depends(get_db)):
    result = create_content_block(section_id, request, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Section not found"
            )
    
    return result   

@router.get('/section/{section_id}/content_blocks')
def get_content_blocks_by_section_id_route(section_id: int, db: Session = Depends(get_db)):
    result = get_content_blocks_by_section_id(section_id, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Section not found"
            )
    
    return result

@router.get('/section/{section_id}/content_blocks/{content_block_id}')
def get_content_block_by_section_id_and_content_block_id_route(section_id: int, content_block_id: int, db: Session = Depends(get_db)):
    result = get_content_block(section_id, content_block_id, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Content block not found"
            )
    
    return result

@router.put('/section/{section_id}/content_blocks/{content_block_id}', response_model=ContentBlockUpdate)
def update_content_block_by_section_id_and_content_block_id(section_id: int, content_block_id: int, request: ContentBlockUpdate, db: Session = Depends(get_db)):
    result = update_content_block(section_id, content_block_id, request, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Content block not found"
            )
    
    return result

@router.delete('/section/{section_id}/content_blocks/{content_block_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_content_block_by_section_id_and_content_block_id(section_id: int, content_block_id: int, db: Session = Depends(get_db)):
    result = delete_content_block(section_id, content_block_id, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Content block not found"
            )
    
    return result
