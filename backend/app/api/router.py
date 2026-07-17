from fastapi import APIRouter
from app.api import events, query, ask

api_router = APIRouter()

api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(query.router, prefix="/query", tags=["query"])
api_router.include_router(ask.router, prefix="/ask", tags=["ask"])
