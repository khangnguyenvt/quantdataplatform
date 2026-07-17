import requests
import pandas as pd
from typing import Optional, Dict, Any, List

class QuantDataClient:
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url.rstrip('/')
        
    def get_events(
        self, 
        event_type: Optional[str] = None,
        ticker: Optional[str] = None,
        sector: Optional[str] = None,
        limit: int = 1000
    ) -> pd.DataFrame:
        """Fetch structured events into a pandas DataFrame."""
        params = {"page_size": min(limit, 500)}
        if event_type: params["event_type"] = event_type
        if ticker: params["ticker"] = ticker
        if sector: params["sector"] = sector
            
        events = []
        page = 1
        
        while len(events) < limit:
            params["page"] = page
            resp = requests.get(f"{self.base_url}/events", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            page_events = data.get("events", [])
            if not page_events:
                break
                
            events.extend(page_events)
            page += 1
            
        if not events:
            return pd.DataFrame()
            
        # Flatten the structured_fields JSON into columns
        df = pd.json_normalize(events)
        
        # Convert dates
        if 'published_at' in df.columns:
            df['published_at'] = pd.to_datetime(df['published_at'])
        if 'content_date' in df.columns:
            df['content_date'] = pd.to_datetime(df['content_date'])
            
        return df.head(limit)
        
    def query(self, sql: str) -> pd.DataFrame:
        """Execute a raw SQL query against the events table."""
        resp = requests.post(
            f"{self.base_url}/query", 
            json={"sql": sql}
        )
        resp.raise_for_status()
        return pd.DataFrame(resp.json())
        
    def ask(self, question: str) -> Dict[str, Any]:
        """Ask a natural language question and get a response + SQL + data."""
        resp = requests.post(
            f"{self.base_url}/ask",
            json={"question": question}
        )
        resp.raise_for_status()
        
        data = resp.json()
        if data.get("events"):
            data["df"] = pd.DataFrame(data["events"])
        else:
            data["df"] = pd.DataFrame()
            
        return data
        
    def semantic_search(self, q: str, limit: int = 10) -> pd.DataFrame:
        """Search events using vector embeddings."""
        resp = requests.get(
            f"{self.base_url}/query/semantic",
            params={"q": q, "limit": limit}
        )
        resp.raise_for_status()
        
        events = resp.json()
        if not events:
            return pd.DataFrame()
            
        df = pd.json_normalize(events)
        return df
