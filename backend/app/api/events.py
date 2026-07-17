from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from app.database import get_db
from app.models.event import Event
from app.schemas.event import EventResponse, EventListResponse

router = APIRouter()

@router.get("", response_model=EventListResponse)
async def list_events(
    event_type: Optional[str] = None,
    ticker: Optional[str] = None,
    source: Optional[str] = None,
    sector: Optional[str] = None,
    published_after: Optional[datetime] = None,
    published_before: Optional[datetime] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_db)
):
    query = select(Event)
    
    if event_type:
        query = query.where(Event.event_type == event_type)
    if ticker:
        query = query.where(Event.ticker == ticker)
    if source:
        query = query.where(Event.source == source)
    if sector:
        query = query.where(Event.sector == sector)
    if published_after:
        query = query.where(Event.published_at >= published_after)
    if published_before:
        query = query.where(Event.published_at <= published_before)
        
    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)
    
    # Get paginated results
    query = query.order_by(desc(Event.published_at)).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    events = result.scalars().all()
    
    return EventListResponse(
        events=list(events),
        total=total or 0,
        page=page,
        page_size=page_size
    )

@router.get("/tickers", response_model=List[str])
async def list_tickers(db: AsyncSession = Depends(get_db)):
    query = select(Event.ticker).where(Event.ticker.is_not(None)).distinct()
    result = await db.execute(query)
    return [t for t in result.scalars().all()]

@router.get("/types", response_model=List[str])
async def list_types(db: AsyncSession = Depends(get_db)):
    query = select(Event.event_type).distinct()
    result = await db.execute(query)
    return [t for t in result.scalars().all()]

@router.get("/sources")
async def list_sources(db: AsyncSession = Depends(get_db)):
    query = select(
        Event.source,
        func.count(Event.id).label('count'),
        func.min(Event.published_at).label('min_date'),
        func.max(Event.published_at).label('max_date')
    ).group_by(Event.source)
    
    result = await db.execute(query)
    return [{"source": r[0], "count": r[1], "min_date": r[2], "max_date": r[3]} for r in result.all()]

@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: UUID, db: AsyncSession = Depends(get_db)):
    query = select(Event).where(Event.id == event_id)
    result = await db.execute(query)
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
