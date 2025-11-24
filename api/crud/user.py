from sqlalchemy.orm import Session

from api.models import User, Profile


def create_user(request: dict, db: Session):
    new_user = User(
        email=request.email,
        role=request.role
    )
    db.add(new_user)
    db.flush()

    profile = Profile(
        first_name=request.first_name,
        last_name=request.last_name,
        bio=request.bio,
        user_id=new_user.id
    )
    db.add(profile)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    return user

def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user

def get_all_users(db: Session, limit: int = 100):
    users = db.query(User).limit(limit).all()
    return users

def delete_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False