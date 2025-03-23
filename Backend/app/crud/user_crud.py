from sqlalchemy.orm import Session
from app.models.users_model import User
from app.schemas.user_schema import UserCreate
from app.core.security import get_password_hash, verify_password

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username = user.username, hashed_password = hashed_password, role_id = user.role_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user.__dict__

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def get_support_members(db: Session):
    support_member_role_id = 2
    return db.query(User).filter(User.role_id == support_member_role_id).all()