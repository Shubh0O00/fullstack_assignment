from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.modules.tickets.helpers import (
    create_ticket_helper,
    update_ticket_status_helper,
    view_tickets_helper,
    edit_ticket_helper,
    assign_ticket_helper,
)
from app.models.tickets_model import TicketStatus

class TicketController:
    @staticmethod
    def create_ticket(ticket_data, db: Session, customer_id: int):
        try:
            return create_ticket_helper(ticket_data, db, customer_id)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @staticmethod
    def change_ticket_status(ticket_id: int, new_status: TicketStatus, db: Session):
        try:
            return update_ticket_status_helper(ticket_id, new_status, db)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @staticmethod
    def view_tickets(filters, db: Session, current_user):
        return view_tickets_helper(filters, db, current_user)

    @staticmethod
    def edit_ticket(ticket_id: int, updated_data, db: Session, customer_id: int):
        try:
            return edit_ticket_helper(ticket_id, updated_data, db, customer_id)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    @staticmethod
    def assign_ticket(ticket_id: int, assigned_to_id: int, db: Session):
        try:
            return assign_ticket_helper(ticket_id, assigned_to_id, db)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
