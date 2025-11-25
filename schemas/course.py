from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum

class CourseCreate(BaseModel):
    title: str
    description: str
    teacher_id: int

class CourseShow(BaseModel):
    id: int
    description: str
    teacher_id: int
    created_at: datetime
    updated_at: datetime

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class SectionCreate(BaseModel):
    title: str
    order_index: int

class SectionShow(BaseModel):
    id: int
    title: str
    order_index: int
    course_id: int

class SectionUpdate(BaseModel):
    title: Optional[str] = None
    order_index: Optional[int] = None

class ContentType(str, Enum):
    lesson = 'lesson'
    assignment = 'assignment'
    quiz = 'quiz'

class ContentBlockBase(BaseModel):
    title: str
    content_type: ContentType
    order_index: int
    url: Optional[str] = None
    content: Optional[str] = None
    duration_minutes: Optional[int] = None
    is_required: bool = True
    requires_grading: bool = False

class ContentBlockCreate(ContentBlockBase):
    pass

class ContentBlockUpdate(BaseModel):
    title: Optional[str] = None
    content_type: Optional[ContentType] = None
    order_index: Optional[int] = None
    url: Optional[str] = None
    content: Optional[str] = None
    duration_minutes: Optional[int] = None
    is_required: Optional[bool] = None
    requires_grading: Optional[bool] = None

class ContentBlockResponse(ContentBlockBase):
    id: int
    section_id: int

class StudentCourse(BaseModel):
    student_id: int
    course_id: int
    enrolled_at: datetime
    progress_percentage: int


class StudentCourseResponse(BaseModel):
    student_id: int
    course_id: int
    enrolled_at: datetime
    progress_percentage: int

class CompletedContentBlockBase(BaseModel):
    url: Optional[str] = None
    grade: Optional[int] = None
    feedback: Optional[str] = None
    section_id: int

class CompletedContentBlockCreate(CompletedContentBlockBase):
    student_id: int
    content_block_id: int

class CompletedContentBlockUpdate(BaseModel):
    url: Optional[str] = None
    grade: Optional[int] = None
    feedback: Optional[str] = None

class CompletedContentBlockResponse(CompletedContentBlockBase):
    student_id: int
    content_block_id: int
    submitted_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
