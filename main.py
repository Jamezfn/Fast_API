from fastapi import FastAPI

from db import get_db, engine
from api.models import Base, User, Course, StudentCourse, Profile, Section, ContentBlock, ContentType, CompletedContentBlock, CompletedSection, CompletedCourse
from api.routers import user, course

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(course.router)