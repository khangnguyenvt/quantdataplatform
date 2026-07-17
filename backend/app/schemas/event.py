from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class EventResponse(BaseModel):
    id: UUID
    event_type: str
    source: str
    entity_name: str
    ticker: Optional[str] = None
    sector: Optional[str] = None
    published_at: datetime
    content_date: Optional[datetime] = None
    headline: Optional[str] = None
    structured_fields: Dict[str, Any]
    raw_text: Optional[str] = None
    ai_signals: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class EventListResponse(BaseModel):
    events: List[EventResponse]
    total: int
    page: int
    page_size: int

class QueryRequest(BaseModel):
    sql: str

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    sql_generated: Optional[str] = None
    events: List[Dict[str, Any]]
