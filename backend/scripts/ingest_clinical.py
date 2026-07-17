import asyncio
import sys
import os

# Add backend dir to python path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import async_session_maker
from app.ingestion.clinical_trials import ClinicalTrialsIngester

async def main():
    print("Starting ClinicalTrials ingestion run...")
    async with async_session_maker() as db:
        ingester = ClinicalTrialsIngester(db)
        try:
            # For daily/hourly cron, 1 day lookback is plenty
            await ingester.ingest(since_days=2)
        finally:
            await ingester.close()
    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())
