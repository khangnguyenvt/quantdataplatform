from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from typing import List, Dict, Any

from app.database import get_db
from app.schemas.event import QueryRequest, EventResponse
from app.models.event import Event
from app.ai.embeddings import embeddings_gen

router = APIRouter()

@router.post("")
async def execute_query(request: QueryRequest, db: AsyncSession = Depends(get_db)) -> List[Dict[str, Any]]:
    sql = request.sql.strip()
    
    # Basic safety check
    if not sql.lower().startswith("select"):
        raise HTTPException(status_code=400, detail="Only SELECT queries are allowed")
        
    forbidden_keywords = ["insert", "update", "delete", "drop", "alter", "truncate", "grant", "revoke"]
    sql_lower = sql.lower()
    if any(keyword in sql_lower for keyword in forbidden_keywords):
         raise HTTPException(status_code=400, detail="Query contains forbidden keywords")
         
    try:
        # Run read-only query
        result = await db.execute(text(sql))
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.all()]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Query execution failed: {str(e)}")

@router.get("/semantic", response_model=List[EventResponse])
async def semantic_search(
    q: str = Query(..., description="Natural language search query"),
    limit: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db)
):
    embedding = embeddings_gen.generate_embedding(q)
    if not embedding:
        raise HTTPException(status_code=500, detail="Failed to generate embedding for query")
        
    # Use pgvector cosine distance operator `<=>`
    query = select(Event).order_by(Event.embedding.cosine_distance(embedding)).limit(limit)
    
    result = await db.execute(query)
    events = result.scalars().all()
    
    return events
