from sqlalchemy.orm import Session
from app.crud.ticket_crud import *
from app.schemas.ticket_schema import TicketCreate, TicketEdit
from app.models.tickets_model import TicketStatus

def create_ticket_helper(ticket_data: TicketCreate, db: Session, customer_id: int):
    # TODO: Implement ticket assignment strategy here (assign to available support member)
    return create_ticket(db, ticket_data, customer_id)

def update_ticket_status_helper(ticket_id: int, new_status: TicketStatus, db: Session):
    ticket = update_ticket_status(db, ticket_id, new_status)
    if not ticket:
        raise Exception("Ticket not found")
    return ticket

def view_tickets_helper(filters, db: Session, current_user):
    if current_user.role_id == 1:
        filters["owner_id"] = current_user.id
    if current_user.role_id == 2:
        filters["assigned_to_id"] = current_user.id
    return get_filtered_tickets(db, filters)

def edit_ticket_helper(ticket_id: int, updated_data: TicketEdit, db: Session, customer_id: int):
    ticket = get_ticket_by_id(db, ticket_id)
    if not ticket:
        raise Exception("Ticket not found")

    if ticket.owner_id != customer_id:
        raise Exception("You can only edit your own tickets")

    return update_ticket(db, ticket_id, updated_data)

def assign_ticket_helper(ticket_id: int, assigned_to_id: int, db: Session):
    ticket = update_ticket_assignment(db, ticket_id, assigned_to_id)
    if not ticket:
        raise Exception("Ticket not found")
    return ticket