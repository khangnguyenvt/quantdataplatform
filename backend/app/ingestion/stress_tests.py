import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.event import Event

# Known BHCs tested in DFAST/CCAR
BANK_TICKERS = {
    "JPMorgan Chase & Co.": "JPM",
    "Bank of America Corporation": "BAC",
    "Citigroup Inc.": "C",
    "Wells Fargo & Company": "WFC",
    "Goldman Sachs Group, Inc., The": "GS",
    "Morgan Stanley": "MS",
    "U.S. Bancorp": "USB",
    "PNC Financial Services Group, Inc., The": "PNC",
    "Truist Financial Corporation": "TFC",
    "Charles Schwab Corporation, The": "SCHW",
    "Capital One Financial Corporation": "COF",
    "State Street Corporation": "STT",
    "Bank of New York Mellon Corporation, The": "BK",
    "American Express Company": "AXP",
    "Northern Trust Corporation": "NTRS",
    "Citizens Financial Group, Inc.": "CFG",
    "Fifth Third Bancorp": "FITB",
    "KeyCorp": "KEY",
    "M&T Bank Corporation": "MTB",
    "Regions Financial Corporation": "RF",
    "Huntington Bancshares Incorporated": "HBAN",
    "Ally Financial Inc.": "ALLY",
    "Discover Financial Services": "DFS"
}

class StressTestIngester:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def ingest_file(self, file_path: str, test_year: int) -> int:
        print(f"Parsing Fed stress test results for {test_year} from {file_path}")
        
        try:
            # For MVP, we simulate parsing since the actual Fed Excel format changes slightly year to year.
            # We would use pd.read_excel(file_path, sheet_name="Projected Capital Ratios")
            # For this MVP implementation, we assume a cleaned or standard structure:
            df = pd.read_excel(file_path)
            # Normalize column names
            df.columns = [str(c).lower().strip() for c in df.columns]
        except Exception as e:
            print(f"Failed to read Excel file: {e}")
            return 0
            
        new_events = 0
        # Assume release dates are usually late June
        published_at = datetime(test_year, 6, 26)
        content_date = datetime(test_year - 1, 12, 31) # Q4 of previous year is the scenario start
        
        for _, row in df.iterrows():
            bhc_name = row.get("bhc name", "Unknown")
            if pd.isna(bhc_name) or "Total" in str(bhc_name):
                continue
                
            ticker = BANK_TICKERS.get(str(bhc_name).strip())
            
            # Use basic defaults if columns are missing in a particular sheet
            pre_stress = float(row.get("actual cet1", 0.0))
            post_stress = float(row.get("minimum cet1", 0.0))
            
            # Check if exists
            existing_query = select(Event.id).where(
                Event.event_type == "stress_test_result",
                Event.source == "fed_ccar",
                Event.structured_fields["bank_name"].astext == str(bhc_name),
                Event.structured_fields["test_year"].astext == str(test_year)
            )
            existing = await self.db.scalar(existing_query)
            if existing:
                continue
                
            headline = f"{bhc_name} Fed {test_year} Stress Test: {post_stress*100:.1f}% min CET1"
            
            structured_fields = {
                "bank_name": str(bhc_name),
                "test_year": test_year,
                "test_type": "DFAST",
                "scenario_type": "severely_adverse",
                "pre_stress_cet1": pre_stress,
                "post_stress_cet1": post_stress,
                "stress_capital_buffer": float(row.get("scb", 0.025)),
                "regulatory_minimum_cet1": 0.045,
                "excess_capital": post_stress - 0.045
            }
            
            event = Event(
                event_type="stress_test_result",
                source="fed_ccar",
                entity_name=str(bhc_name),
                ticker=ticker,
                sector="Financials",
                published_at=published_at,
                content_date=content_date,
                headline=headline,
                structured_fields=structured_fields,
                raw_text=f"Parsed from Fed results for {test_year}",
                embedding=None
            )
            
            self.db.add(event)
            new_events += 1
            
        await self.db.commit()
        print(f"Successfully ingested {new_events} stress test events.")
        return new_events
