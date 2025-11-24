from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Index, SmallInteger, String, Integer, Enum, Text, UniqueConstraint, func
import enum

from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .user import User

class ContentType(enum.Enum):
    lesson = 'lesson'
    assignment = 'assignment'
    quiz = 'quiz'

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    student_courses: Mapped[list["StudentCourse"]] = relationship("StudentCourse", back_populates="course", cascade="all, delete-orphan")
    teacher: Mapped["User"] = relationship("User", back_populates="courses_taught")
    sections: Mapped[list["Section"]] = relationship("Section", back_populates="course", cascade="all, delete-orphan", order_by="Section.id")
    completed_courses: Mapped[list["CompletedCourse"]] = relationship("CompletedCourse", back_populates="course", cascade="all, delete-orphan")

class Section(Base):
    __tablename__ = "sections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("courses.id"), nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)  

    course: Mapped["Course"] = relationship("Course", back_populates="sections")
    content_blocks: Mapped[list["ContentBlock"]] = relationship("ContentBlock", back_populates="section", cascade="all, delete-orphan", order_by="ContentBlock.id")
    completed_by_students: Mapped[list["CompletedSection"]] = relationship("CompletedSection", back_populates="section", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('course_id', 'order_index', name='uq_course_section_order'),
        Index('ix_section_course_order', 'course_id', 'order_index'),
    )

class ContentBlock(Base):
    __tablename__ = "content_blocks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content_type: Mapped[ContentType] = mapped_column(
        Enum(ContentType, name="content_type_enum", native_enum=False), nullable=False)
    section_id: Mapped[int] = mapped_column(Integer, ForeignKey("sections.id"), nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)

    url: Mapped[str | None] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)

    is_required: Mapped[bool] = mapped_column(Boolean, default=True)
    requires_grading: Mapped[bool] = mapped_column(Boolean, default=False)

    section: Mapped["Section"] = relationship("Section", back_populates="content_blocks")
    completed_by_students: Mapped[list["CompletedContentBlock"]] = relationship(
        "CompletedContentBlock", back_populates="content_block", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint('section_id', 'order_index', name='uq_section_order'),
        CheckConstraint('order_index >= 0', name='ck_order_index_positive'),
    )

class StudentCourse(Base):
    __tablename__ = "student_courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    progress_percentage: Mapped[int] = mapped_column(SmallInteger, default=0)

    student: Mapped["User"] = relationship("User", back_populates="student_courses")
    course: Mapped["Course"] = relationship("Course", back_populates="student_courses")

    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', name='uq_student_course'),
        CheckConstraint('progress_percentage >= 0 AND progress_percentage <= 100', name='ck_progress_percentage_range'),
    )


class CompletedContentBlock(Base):
    __tablename__ = "completed_content_blocks"

    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    content_block_id: Mapped[int] = mapped_column(Integer, ForeignKey("content_blocks.id"), primary_key=True)
    url: Mapped[str | None] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    grade: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    section_id: Mapped[int] = mapped_column(Integer, ForeignKey("sections.id"), nullable=False)
    
    student: Mapped["User"] = relationship("User", back_populates="completed_content_blocks")
    content_block: Mapped["ContentBlock"] = relationship(
        "ContentBlock", back_populates="completed_by_students")
    
    __table_args__ = (
        Index('ix_student_contentblock', 'student_id', 'content_block_id'),
        CheckConstraint('grade >= 0 AND grade <= 100', name='ck_completed_content_grade_range'),
    )
    
class CompletedSection(Base):
    __tablename__ = "completed_sections"

    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    section_id: Mapped[int] = mapped_column(Integer, ForeignKey("sections.id"), primary_key=True)
    completed_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    student: Mapped["User"] = relationship("User", back_populates="completed_sections")
    section: Mapped["Section"] = relationship("Section", back_populates="completed_by_students")

class CompletedCourse(Base):
    __tablename__ = "completed_courses"

    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("courses.id"), primary_key=True)
    completed_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    final_grade: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    certificate_issued: Mapped[bool] = mapped_column(Boolean, default=False)
    certificate_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    student: Mapped["User"] = relationship("User", back_populates="completed_courses")
    course: Mapped["Course"] = relationship("Course", back_populates="completed_courses")

    __table_args__ = (
        CheckConstraint('final_grade >= 0 AND final_grade <= 100', name='ck_completed_course_final_grade_range'),
    )