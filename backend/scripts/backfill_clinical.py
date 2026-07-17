import asyncio
import sys
import os

# Add backend dir to python path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import async_session_maker
from app.ingestion.clinical_trials import ClinicalTrialsIngester

async def main():
    print("Starting Historical Backfill for ClinicalTrials (last 12 months)...")
    async with async_session_maker() as db:
        ingester = ClinicalTrialsIngester(db)
        try:
            # 365 days lookback for initial backfill
            await ingester.ingest(since_days=365)
        finally:
            await ingester.close()
    print("Backfill Complete.")

if __name__ == "__main__":
    asyncio.run(main())
