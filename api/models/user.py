from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Boolean, ForeignKey, String, Integer, Enum, Text
import enum

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
    
    profile: Mapped["Profile"] = relationship("Profile", back_populates="owner", uselist=False)

class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="profile")