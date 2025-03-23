from pydantic import BaseModel
from typing import Optional
from app.models.tickets_model import TicketStatus

class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None

class TicketCreate(TicketBase):
    pass

class TicketRead(TicketBase):
    id: int
    status: TicketStatus
    owner_id: int
    assigned_to_id: Optional[int] = None

    class Config:
        orm_mode = True

class TicketEdit(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True

class TicketUpdateStatus(BaseModel):
    status: str

class TicketAssign(BaseModel):
    assigned_to_id: int
