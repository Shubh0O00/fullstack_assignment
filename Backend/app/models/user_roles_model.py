from sqlalchemy import Column, Integer, String
from app.core.database import Base

class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, index=True, nullable=False)  # ✅ Added VARCHAR(50)
