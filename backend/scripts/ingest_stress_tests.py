import asyncio
import sys
import os
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import async_session_maker
from app.ingestion.stress_tests import StressTestIngester

async def main():
    parser = argparse.ArgumentParser(description="Ingest Fed Stress Test Excel")
    parser.add_argument("--file", required=True, help="Path to the Excel file")
    parser.add_argument("--year", required=True, type=int, help="Stress test year")
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"File not found: {args.file}")
        sys.exit(1)

    print(f"Starting Stress Test ingestion for {args.year}...")
    async with async_session_maker() as db:
        ingester = StressTestIngester(db)
        await ingester.ingest_file(args.file, args.year)
    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())
