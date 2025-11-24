from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"

class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.student

class UserCreate(UserBase):
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "student@example.com",
                "role": "student"
            }
        }
    }

class ShowUser(UserBase):
    id: int
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }