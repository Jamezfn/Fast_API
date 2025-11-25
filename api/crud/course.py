from sqlalchemy.orm import Session

from api.models import (User, Profile, Course, UserRole, 
                        Section, ContentBlock, StudentCourse, CompletedContentBlock)

def create_course(request: dict, db: Session):
    course = db.query(Course).filter(Course.title == request.title).first()
    if course:
        return None
    
    teacher = db.query(User).filter(User.id == request.teacher_id, User.role == UserRole.teacher).first()

    if not teacher:
        return None
    
    new_course = Course(
        description=request.description,
        title=request.title,
        teacher_id=teacher.id
    )

    db.add(new_course)
    db.commit()

    return new_course

def get_course(course_id: int, db: Session):
    return db.query(Course).filter(Course.id == course_id).first()

def get_courses(db: Session):
    return db.query(Course).all()

def update_course(course_id: int, request: dict, db: Session):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        return None
    
    course.title = request.title
    course.description = request.description
    db.commit()
    return course

def delete_course(course_id: int, db: Session):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        return None
    
    db.delete(course)
    db.commit()
    return course

def get_course_by_teacher(teacher_id: int, db: Session):
    return db.query(Course).filter(Course.teacher_id == teacher_id).all()

def create_section(course_id: int, section: dict, db: Session):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        return None
    
    new_section = Section(
        title=section.title,
        order_index=section.order_index,
        course_id=course_id
    )
    
    db.add(new_section)
    db.commit()
    return new_section

def get_section(section_id: int, db: Session):
    return db.query(Section).filter(Section.id == section_id).first()

def update_section(section_id: int, request: dict, db: Session):
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        return None
    
    section.title = request.title
    section.description = request.description
    section.order_index = request.order_index
    db.commit()
    return section

def delete_section(section_id: int, db: Session):
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        return None
    
    db.delete(section)
    db.commit()
    return section

def create_content_block(section_id: int, content_block: dict, db: Session):
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        return None
    
    new_content_block = ContentBlock(
        title=content_block.title,
        content_type=content_block.content_type,
        order_index=content_block.order_index,
        url=content_block.url,
        content=content_block.content,
        duration_minutes=content_block.duration_minutes,
        section_id=section_id
    )
    
    db.add(new_content_block)
    db.commit()
    return new_content_block

def get_content_block(content_block_id: int, db: Session):
    return db.query(ContentBlock).filter(ContentBlock.id == content_block_id).first()

def update_content_block(content_block_id: int, request: dict, db: Session):
    content_block = db.query(ContentBlock).filter(ContentBlock.id == content_block_id).first()
    if not content_block:
        return None
    
    content_block.title = request.title
    content_block.description = request.description
    db.commit()
    return content_block

def delete_content_block(content_block_id: int, db: Session):
    content_block = db.query(ContentBlock).filter(ContentBlock.id == content_block_id).first()
    if not content_block:
        return None
    
    db.delete(content_block)
    db.commit()
    return content_block

def get_all_content_blocks(db: Session):
    return db.query(ContentBlock).all()

def get_content_blocks_by_section_id(section_id: int, db: Session):
    return db.query(ContentBlock).filter(ContentBlock.section_id == section_id).all()


def enroll_student(student_id: int, course_id: int, db: Session):
    enrolled = db.query(StudentCourse).filter(StudentCourse.student_id == student_id, StudentCourse.course_id == course_id).first()
    if enrolled:
        return None 
    student_course = StudentCourse(
        student_id=student_id,
        course_id=course_id,
    )
    db.add(student_course)
    db.commit()

    return student_course
