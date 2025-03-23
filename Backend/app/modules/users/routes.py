from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.modules.users.controllers import UserController
from app.schemas.user_schema import UserCreate, Token, UserInDB
from app.core.dependencies import get_db  
from app.core.security import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

router = APIRouter()

@router.post("/register", response_model=UserInDB)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserController.register_user(user, db)

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return UserController.login_user(form_data.username, form_data.password, db)

@router.get("/me", response_model=UserInDB)
def read_me(current_user: UserInDB = Depends(get_current_user)):
    return UserController.get_me(current_user)

@router.get("/support_members", response_model=List[UserInDB])
def get_support_members(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return UserController.get_support_members(db, current_user)
