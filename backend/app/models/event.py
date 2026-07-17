from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector
from uuid import uuid4
from app.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    event_type = Column(String, nullable=False, index=True)
    # event_type values: patent_filed, patent_granted, trademark_filed,
    #   fcc_filing, trial_registered, trial_status_change,
    #   trial_completed, trial_terminated, stress_test_result,
    #   bond_issued, rating_action

    source = Column(String, nullable=False)
    # source values: clinicaltrials_gov, patentsview, uspto_tess,
    #   fcc_oet, fed_ccar, eba_stress, finra_trace, sec_edgar

    entity_name = Column(String, nullable=False, index=True)
    ticker = Column(String, nullable=True, index=True)
    sector = Column(String, nullable=True)

    published_at = Column(DateTime(timezone=True), nullable=False, index=True)
    # CRITICAL: This is when the data became PUBLICLY KNOWABLE.
    # NOT the content date. This is what makes backtests valid.

    content_date = Column(DateTime(timezone=True), nullable=True)
    # The date the data refers to (e.g., patent application date)

    headline = Column(Text, nullable=True)
    # AI-generated 1-line summary

    structured_fields = Column(JSONB, nullable=False, default=dict)
    # Vertical-specific fields (see schema in plan)

    raw_text = Column(Text, nullable=True)
    # Original filing/document text

    embedding = Column(Vector(768), nullable=True)
    # Gemini text-embedding-004 produces 768-dim vectors

    ai_signals = Column(JSONB, nullable=True, default=dict)
    # Extracted signals: sentiment, anomaly flags, PoS, etc.

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
