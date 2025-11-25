from sqlalchemy.orm import Session

from api.models import User, Profile, Course, UserRole, Section


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