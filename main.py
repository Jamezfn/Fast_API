from fastapi import FastAPI

from db import get_db, engine
from api.models import Base, User, Course, StudentCourse, Profile, Section, ContentBlock, ContentType, CompletedContentBlock, CompletedSection, CompletedCourse

Base.metadata.create_all(bind=engine)

app = FastAPI()







