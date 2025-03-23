from sqlalchemy.orm import Session
from typing import Optional, Dict
from app.models.tickets_model import Ticket, TicketStatus
from app.schemas.ticket_schema import TicketCreate, TicketEdit

def create_ticket(db: Session, ticket: TicketCreate, owner_id: int, assigned_to_id: Optional[int] = None):
    db_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        owner_id=owner_id,
        assigned_to_id=assigned_to_id
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_ticket_by_id(db: Session, ticket_id: int):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()

def get_filtered_tickets(db: Session, filters: Dict):
    query = db.query(Ticket)
    for key, value in filters.items():
        query = query.filter(getattr(Ticket, key) == value)
    return query.all()

def update_ticket_status(db: Session, ticket_id: int, status: TicketStatus, assigned_to_id: Optional[int] = None):
    ticket = get_ticket_by_id(db, ticket_id)
    if not ticket:
        return None
    ticket.status = status
    if status == TicketStatus.PICKED and assigned_to_id:
        ticket.assigned_to_id = assigned_to_id
    if status == TicketStatus.ESCALATED:
        ticket.assigned_to_id = None
    db.commit()
    db.refresh(ticket)
    return ticket

def update_ticket(db: Session, ticket_id: int, updated_data: TicketEdit):
    ticket = get_ticket_by_id(db, ticket_id)
    if not ticket:
        return None
    if updated_data.title:
        ticket.title = updated_data.title
    if updated_data.description:
        ticket.description = updated_data.description
    db.commit()
    db.refresh(ticket)
    return ticket

def update_ticket_assignment(db: Session, ticket_id: int, assigned_to_id: int):
    ticket = get_ticket_by_id(db, ticket_id)
    if not ticket:
        return None
    ticket.assigned_to_id = assigned_to_id
    db.commit()
    db.refresh(ticket)
    return ticket
