from sqlalchemy.orm import Session

from api.models import User, Profile, Course, UserRole

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