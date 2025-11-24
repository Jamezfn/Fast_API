from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, ForeignKey, String, Integer, Enum, Text, DateTime, func

from datetime import datetime
import enum

from api.models.course import CompletedContentBlock, CompletedCourse, CompletedSection, Course, StudentCourse
from base import Base

class UserRole(enum.Enum):
    teacher = 'teacher'
    student = 'student'

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_roles_enum", native_enum=False), default=UserRole.student, nullable=False) 
    
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    profile: Mapped["Profile"] = relationship("Profile", back_populates="owner", uselist=False)
    completed_content_blocks: Mapped[list["CompletedContentBlock"]] = relationship("CompletedContentBlock", back_populates="student", cascade="all, delete-orphan")
    courses_taught: Mapped[list["Course"]] = relationship("Course", back_populates="teacher", cascade="all, delete-orphan")
    student_courses: Mapped[list["StudentCourse"]] = relationship("StudentCourse", back_populates="student", cascade="all, delete-orphan")
    completed_sections: Mapped[list["CompletedSection"]] = relationship("CompletedSection", back_populates="student", cascade="all, delete-orphan")
    completed_courses: Mapped[list["CompletedCourse"]] = relationship("CompletedCourse", back_populates="student", cascade="all, delete-orphan")

class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="profile")