from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from enum import Enum
from typing import Optional

class UserRole(str, Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"

class UserBase(BaseModel):
    first_name: str
    last_name: str
    bio: str | None = None
    email: EmailStr
    role: UserRole = UserRole.student

class UserCreate(UserBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "bio": "A short bio about John",
                    "email": "student@example.com",
                    "role": "student"
                }
            ]
        }
    )

class ShowProfile(BaseModel):
    id: int
    first_name: str
    last_name: str
    bio: Optional[str] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class ShowUser(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime
    profile: Optional[ShowProfile] = None

    model_config = ConfigDict(from_attributes=True)