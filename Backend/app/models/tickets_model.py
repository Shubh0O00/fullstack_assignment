from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.users_model import User  # ✅ Import User
import enum

class TicketStatus(enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PICKED = "picked"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    CLOSED = "closed"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), index=True, nullable=False)  # ✅ Added VARCHAR(255)
    description = Column(String(1000), nullable=True)  # ✅ VARCHAR(1000) for descriptions

    # ✅ Fix ENUM handling for MySQL
    status = Column(Enum(TicketStatus), nullable=False, default=TicketStatus.OPEN)

    owner_id = Column(Integer, ForeignKey(User.id), nullable=False)  # ✅ MySQL-Compatible FK
    owner = relationship(User, foreign_keys=[owner_id])

    assigned_to_id = Column(Integer, ForeignKey(User.id), nullable=True)  # ✅ Nullable FK
    assigned_to = relationship(User, foreign_keys=[assigned_to_id])
