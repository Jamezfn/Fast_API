from sqlalchemy.orm import Session

from api.models import User


def create_user(request: dict, db: Session):
    new_user = User(
        email=request.email,
        role=request.role
    )
    db.add(new_user)
    db.flush()
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    return user

def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user