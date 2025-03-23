from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role_id: int

class UserInDB(UserBase):
    id: int
    is_active: bool
    role_id: int

    class Config: 
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class UserRole(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
