"""Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2026-07-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import pgvector.sqlalchemy

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Ensure pgvector extension exists
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    
    op.create_table('events',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('event_type', sa.String(), nullable=False),
    sa.Column('source', sa.String(), nullable=False),
    sa.Column('entity_name', sa.String(), nullable=False),
    sa.Column('ticker', sa.String(), nullable=True),
    sa.Column('sector', sa.String(), nullable=True),
    sa.Column('published_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('content_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('headline', sa.Text(), nullable=True),
    sa.Column('structured_fields', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('raw_text', sa.Text(), nullable=True),
    sa.Column('embedding', pgvector.sqlalchemy.Vector(dim=768), nullable=True),
    sa.Column('ai_signals', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_events_entity_name'), 'events', ['entity_name'], unique=False)
    op.create_index(op.f('ix_events_event_type'), 'events', ['event_type'], unique=False)
    op.create_index(op.f('ix_events_published_at'), 'events', ['published_at'], unique=False)
    op.create_index(op.f('ix_events_ticker'), 'events', ['ticker'], unique=False)
    
    # Custom indexes for JSONB and Vector
    op.execute("CREATE INDEX ix_events_event_type_published_at ON events (event_type, published_at)")
    op.execute("CREATE INDEX ix_events_ticker_published_at ON events (ticker, published_at)")
    op.execute("CREATE INDEX ix_events_structured_fields ON events USING GIN (structured_fields)")
    op.execute("CREATE INDEX ix_events_embedding ON events USING hnsw (embedding vector_cosine_ops)")

def downgrade() -> None:
    op.drop_index(op.f('ix_events_ticker'), table_name='events')
    op.drop_index(op.f('ix_events_published_at'), table_name='events')
    op.drop_index(op.f('ix_events_event_type'), table_name='events')
    op.drop_index(op.f('ix_events_entity_name'), table_name='events')
    op.drop_table('events')
