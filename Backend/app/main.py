from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.modules import include_module_routes

app = FastAPI(title="Customer Support Ticketing System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

include_module_routes(app)

@app.get("/")
async def read_root():
    return {"message": "Hello, welcome to the Ticketing System API!"}