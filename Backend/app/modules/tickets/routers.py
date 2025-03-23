from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.modules.tickets.controllers import TicketController
from app.schemas.ticket_schema import TicketRead, TicketCreate, TicketEdit, TicketUpdateStatus, TicketAssign
from app.models.tickets_model import TicketStatus
from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.core.permissions import require_role
from fastapi import HTTPException
from typing import Optional

router = APIRouter()

@router.post("/create", response_model=TicketRead)
def create_ticket(ticket: TicketCreate, 
                  db: Session = Depends(get_db),
                  current_user = Depends(require_role(["customer"]))):
    return TicketController.create_ticket(ticket, db, customer_id=current_user.id)

@router.put("/{ticket_id}/status", response_model=TicketRead)
def change_ticket_status(ticket_id: int, ticket_update_status: TicketUpdateStatus, 
                         db: Session = Depends(get_db),
                         current_user = Depends(require_role(["support_member", "support_manager"]))):
    try:
        new_status = getattr(TicketStatus, ticket_update_status.status.upper())
    except AttributeError:
        raise HTTPException(status_code=400, detail="Invalid status")
    return TicketController.change_ticket_status(ticket_id, new_status, db)

@router.get("/view", response_model=list[TicketRead])
def view_tickets(user_id: Optional[int] = Query(None), status: Optional[str] = Query(None), 
                 db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    filters = {}
    if user_id:
        filters["owner_id"] = user_id
    if status:
        try:
            filters["status"] = TicketStatus[status.upper()]
        except KeyError:
            raise HTTPException(status_code=400, detail="Invalid status")
    
    return TicketController.view_tickets(filters, db, current_user)

@router.put("/{ticket_id}/edit", response_model=TicketRead)
def edit_ticket(ticket_id: int, updated_data: TicketEdit, 
                db: Session = Depends(get_db), current_user = Depends(require_role(["customer"]))):
    return TicketController.edit_ticket(ticket_id, updated_data, db, customer_id=current_user.id)

@router.put("/{ticket_id}/assign", response_model=TicketRead)
def assign_ticket(
    ticket_id: int, 
    assignment: TicketAssign,  
    db: Session = Depends(get_db), 
    current_user = Depends(require_role(["support_manager"]))
):
    return TicketController.assign_ticket(ticket_id, assignment.assigned_to_id, db)
