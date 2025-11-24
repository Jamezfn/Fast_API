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