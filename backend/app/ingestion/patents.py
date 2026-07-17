import httpx
from datetime import datetime, timedelta
import asyncio
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.event import Event
from app.ingestion.entity_resolver import resolver
from app.ai.embeddings import embeddings_gen
from google import genai
from app.config import settings

class PatentsIngester:
    BASE_URL = "https://api.patentsview.org/patents/query"
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.client = httpx.AsyncClient(timeout=30.0)
        if settings.gemini_api_key:
            self.gemini_client = genai.Client(api_key=settings.gemini_api_key)
        else:
            self.gemini_client = None
            
    async def close(self):
        await self.client.aclose()

    def classify_patent(self, abstract: str) -> List[str]:
        if not self.gemini_client or not abstract:
            return []
            
        try:
            prompt = f"Classify this patent abstract into 1-3 technology categories from this list: [AI/ML, Semiconductor, Battery/Energy, Biotech/Pharma, Telecom/5G, Autonomous Vehicles, Cloud/Software, Robotics, Quantum Computing, Other]. Return only the category names separated by commas. Abstract: {abstract}"
            
            response = self.gemini_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            cats = [c.strip() for c in response.text.split(",")]
            return [c for c in cats if c]
        except Exception as e:
            print(f"Error classifying patent: {e}")
            return []

    async def fetch_patents(self, since_date: str) -> List[Dict[str, Any]]:
        # query for patents granted >= since_date
        query = {
            "q": {"_gte": {"patent_date": since_date}},
            "f": ["patent_id", "patent_title", "patent_abstract", "patent_date", "patent_type", 
                  "assignee_organization", "app_date", "cpc_group_id"],
            "o": {"per_page": 1000}
        }
        
        # Note: the actual PatentsView API requires POST with this JSON format
        # and has rate limits.
        all_patents = []
        
        try:
            response = await self.client.post(self.BASE_URL, json=query)
            if response.status_code == 200:
                data = response.json()
                all_patents = data.get("patents", [])
            else:
                print(f"Error from PatentsView API: {response.text}")
        except Exception as e:
            print(f"Exception fetching patents: {e}")
            
        return all_patents

    async def ingest(self, since_days: int = 7) -> int:
        since_date = (datetime.utcnow() - timedelta(days=since_days)).strftime("%Y-%m-%d")
        print(f"Fetching patents granted since {since_date}...")
        
        patents = await self.fetch_patents(since_date)
        if not patents:
            print("No patents found.")
            return 0
            
        print(f"Found {len(patents)} granted patents.")
        
        new_events = 0
        
        for p in patents:
            patent_id = p.get("patent_id")
            if not patent_id:
                continue
                
            published_at_str = p.get("patent_date")
            if not published_at_str:
                continue
                
            try:
                published_at = datetime.strptime(published_at_str, "%Y-%m-%d")
            except:
                continue
                
            # Check if exists
            existing_query = select(Event.id).where(
                Event.event_type == "patent_granted",
                Event.source == "patentsview",
                Event.structured_fields["patent_id"].astext == patent_id
            )
            existing = await self.db.scalar(existing_query)
            if existing:
                continue
                
            assignees = p.get("assignees", [])
            assignee_org = assignees[0].get("assignee_organization") if assignees else "Unknown"
            ticker = resolver.resolve_ticker(assignee_org)
            
            title = p.get("patent_title", "")
            abstract = p.get("patent_abstract", "")
            
            headline = f"{assignee_org} granted patent for: {title}"
            
            apps = p.get("applications", [])
            app_date_str = apps[0].get("app_date") if apps else None
            content_date = None
            if app_date_str:
                try:
                    content_date = datetime.strptime(app_date_str, "%Y-%m-%d")
                except:
                    pass
                    
            cpcs = p.get("cpcs", [])
            cpc_codes = [c.get("cpc_group_id") for c in cpcs if c.get("cpc_group_id")]
            
            clusters = self.classify_patent(abstract)
            
            raw_text = f"Title: {title}\nAbstract: {abstract}"
            
            embedding = None
            if since_days <= 14:
                embedding = embeddings_gen.generate_embedding(raw_text)
                
            structured_fields = {
                "patent_id": patent_id,
                "patent_title": title,
                "application_date": app_date_str,
                "grant_date": published_at_str,
                "assignee": assignee_org,
                "patent_type": p.get("patent_type", "utility"),
                "technology_clusters": clusters,
                "cpc_codes": cpc_codes
            }
            
            event = Event(
                event_type="patent_granted",
                source="patentsview",
                entity_name=assignee_org,
                ticker=ticker,
                sector="Technology", # naive default, could improve
                published_at=published_at,
                content_date=content_date,
                headline=headline,
                structured_fields=structured_fields,
                raw_text=raw_text,
                embedding=embedding
            )
            
            self.db.add(event)
            new_events += 1
            
            if new_events % 20 == 0:
                await self.db.commit()
                
        await self.db.commit()
        print(f"Successfully ingested {new_events} new patent events.")
        return new_events
