import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import async_session_maker
from app.ingestion.patents import PatentsIngester

async def main():
    print("Starting Patents ingestion run...")
    async with async_session_maker() as db:
        ingester = PatentsIngester(db)
        try:
            # Weekly cron, check last 7 days
            await ingester.ingest(since_days=7)
        finally:
            await ingester.close()
    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())
