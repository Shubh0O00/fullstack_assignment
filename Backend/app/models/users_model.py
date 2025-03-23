from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.user_roles_model import UserRole  # ✅ Import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, index=True, nullable=False)  # ✅ Added VARCHAR(100)
    hashed_password = Column(String(255), nullable=False)  # ✅ VARCHAR(255) for hashed passwords
    is_active = Column(Boolean, default=True)

    role_id = Column(Integer, ForeignKey(UserRole.id), nullable=False)  # ✅ MySQL-Compatible FK
    role = relationship(UserRole)  # ✅ ORM Relationship
