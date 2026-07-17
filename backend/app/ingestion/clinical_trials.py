import httpx
from datetime import datetime, timedelta
import asyncio
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.event import Event
from app.ingestion.entity_resolver import resolver
from app.ai.summarizer import summarizer
from app.ai.embeddings import embeddings_gen

class ClinicalTrialsIngester:
    BASE_URL = "https://clinicaltrials.gov/api/v2/studies"
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def close(self):
        await self.client.aclose()

    async def fetch_studies(self, since_date: str) -> List[Dict[str, Any]]:
        # format: yyyy-MM-dd
        today = datetime.utcnow().strftime("%Y-%m-%d")
        
        params = {
            "format": "json",
            "filter.advanced": f"AREA[LastUpdatePostDate]RANGE[{since_date},{today}]",
            "fields": "NCTId,BriefTitle,OverallStatus,Phase,EnrollmentCount,StartDate,PrimaryCompletionDate,LeadSponsorName,Condition,LastUpdatePostDate,LastUpdateSubmitDate,BriefSummary,StudyType",
            "pageSize": 1000
        }
        
        all_studies = []
        next_page_token = None
        
        while True:
            if next_page_token:
                params["pageToken"] = next_page_token
                
            try:
                response = await self.client.get(self.BASE_URL, params=params)
                response.raise_for_status()
                data = response.json()
                
                studies = data.get("studies", [])
                all_studies.extend(studies)
                
                next_page_token = data.get("nextPageToken")
                if not next_page_token:
                    break
                    
                # respect rate limits (3 req/sec)
                await asyncio.sleep(0.35)
                
            except Exception as e:
                print(f"Error fetching from ClinicalTrials API: {e}")
                break
                
        return all_studies

    async def ingest(self, since_days: int = 1) -> int:
        since_date = (datetime.utcnow() - timedelta(days=since_days)).strftime("%Y-%m-%d")
        print(f"Fetching studies updated since {since_date}...")
        
        studies = await self.fetch_studies(since_date)
        print(f"Found {len(studies)} updated studies.")
        
        new_events = 0
        
        for study in studies:
            protocol = study.get("protocolSection", {})
            ident = protocol.get("identificationModule", {})
            status_mod = protocol.get("statusModule", {})
            design = protocol.get("designModule", {})
            sponsor_mod = protocol.get("sponsorCollaboratorsModule", {})
            conditions_mod = protocol.get("conditionsModule", {})
            description = protocol.get("descriptionModule", {})
            
            nct_id = ident.get("nctId")
            if not nct_id:
                continue
                
            current_status = status_mod.get("overallStatus", "Unknown")
            published_at_str = status_mod.get("lastUpdatePostDateStruct", {}).get("date")
            if not published_at_str:
                continue
                
            try:
                published_at = datetime.strptime(published_at_str, "%Y-%m-%d")
            except:
                continue
                
            # Check if this exact update is already in DB
            existing_query = select(Event.id).where(
                Event.event_type.in_(["trial_status_change", "trial_registered"]),
                Event.source == "clinicaltrials_gov",
                Event.structured_fields["nct_id"].astext == nct_id,
                Event.published_at == published_at
            )
            existing = await self.db.scalar(existing_query)
            if existing:
                continue # Already ingested this update
                
            # It's a new update.
            # Realistically we should compare with previous status to see if it changed, 
            # but for MVP we'll treat every significant update as a status_change or registered
            
            # Check if we have ANY record of this trial
            any_query = select(Event.structured_fields["status"].astext).where(
                Event.source == "clinicaltrials_gov",
                Event.structured_fields["nct_id"].astext == nct_id
            ).order_by(Event.published_at.desc()).limit(1)
            
            prev_status = await self.db.scalar(any_query)
            
            event_type = "trial_status_change" if prev_status else "trial_registered"
            
            # If it's just a minor update (status didn't change), for an MVP we might still track it,
            # or skip it to save space. We will track it if it's new.
            
            sponsor_name = sponsor_mod.get("leadSponsor", {}).get("name", "Unknown")
            ticker = resolver.resolve_ticker(sponsor_name)
            
            title = ident.get("briefTitle", "")
            phase_list = design.get("phases", [])
            phase = phase_list[0] if phase_list else "Unknown"
            condition_list = conditions_mod.get("conditions", [])
            condition = condition_list[0] if condition_list else "Unknown"
            
            headline = summarizer.generate_clinical_headline(
                title=title, status=current_status, phase=phase, 
                condition=condition, sponsor=sponsor_name
            )
            
            summary_text = description.get("briefSummary", "")
            raw_text = f"Title: {title}\nSummary: {summary_text}"
            
            # For backfill we might skip embeddings to save API costs, but we'll do it for recent
            embedding = None
            if since_days <= 7:
                embedding = embeddings_gen.generate_embedding(raw_text)
                
            content_date_str = status_mod.get("lastUpdateSubmitDate")
            content_date = None
            if content_date_str:
                try:
                    content_date = datetime.strptime(content_date_str, "%Y-%m-%d")
                except:
                    pass
            
            structured_fields = {
                "nct_id": nct_id,
                "sponsor": sponsor_name,
                "phase": phase,
                "status": current_status,
                "previous_status": prev_status,
                "indication": condition,
                "enrollment_actual": status_mod.get("enrollmentCount", 0) if status_mod.get("enrollmentType") == "ACTUAL" else None,
                "enrollment_planned": status_mod.get("enrollmentCount", 0) if status_mod.get("enrollmentType") == "ESTIMATED" else None,
                "primary_completion_date": status_mod.get("primaryCompletionDateStruct", {}).get("date"),
                "study_type": design.get("studyType")
            }
            
            event = Event(
                event_type=event_type,
                source="clinicaltrials_gov",
                entity_name=sponsor_name,
                ticker=ticker,
                sector="Health Care",
                published_at=published_at,
                content_date=content_date,
                headline=headline,
                structured_fields=structured_fields,
                raw_text=raw_text,
                embedding=embedding
            )
            
            self.db.add(event)
            new_events += 1
            
            if new_events % 50 == 0:
                await self.db.commit()
                
        await self.db.commit()
        print(f"Successfully ingested {new_events} new trial events.")
        return new_events
