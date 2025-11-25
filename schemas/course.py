from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

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

    model_config = ConfigDict(from_attributes=True)

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
