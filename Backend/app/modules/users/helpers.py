from app.crud.user_crud import get_user_by_username, create_user, authenticate_user, get_support_members
from app.core.security import create_access_token

def register_user_helper(user_data, db):
    if get_user_by_username(db, user_data.username):
        raise Exception("Username already exists")
    return create_user(db, user_data)

def login_user_helper(username: str, password: str, db):
    user = authenticate_user(db, username, password)
    if not user:
        raise Exception("Incorrect username or password")
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

def get_support_members_helper(db):
    return get_support_members(db)
