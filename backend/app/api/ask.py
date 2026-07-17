from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.schemas.event import AskRequest, AskResponse
from app.database import get_db
from app.ai.sql_translator import sql_translator

router = APIRouter()

@router.post("", response_model=AskResponse)
async def ask_question(request: AskRequest, db: AsyncSession = Depends(get_db)):
    # 1. Translate question to SQL
    sql = sql_translator.translate_to_sql(request.question)
    
    # 2. Basic safety validation
    if not sql.lower().strip().startswith("select"):
        raise HTTPException(status_code=400, detail="Generated query was not a SELECT statement.")
        
    forbidden_keywords = ["insert", "update", "delete", "drop", "alter", "truncate", "grant", "revoke"]
    sql_lower = sql.lower()
    if any(keyword in sql_lower for keyword in forbidden_keywords):
         raise HTTPException(status_code=400, detail="Query contains forbidden keywords")
         
    # 3. Execute the SQL
    try:
        result = await db.execute(text(sql))
        columns = result.keys()
        events = [dict(zip(columns, row)) for row in result.all()]
        
        answer = f"Found {len(events)} results for your query."
        return AskResponse(
            answer=answer,
            sql_generated=sql,
            events=events
        )
    except Exception as e:
        return AskResponse(
            answer=f"Failed to execute query: {str(e)}",
            sql_generated=sql,
            events=[]
        )
