from .users.routes import router as user_router
from .tickets.routers import router as ticket_router

def include_module_routes(app):
    app.include_router(user_router, prefix="/users", tags=["users"])
    app.include_router(ticket_router, prefix="/tickets", tags=["tickets"])