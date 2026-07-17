from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.config import settings

# asyncpg uses 'ssl' instead of 'sslmode'
db_url = settings.database_url.replace("sslmode=", "ssl=")

engine = create_async_engine(
    db_url,
    echo=settings.app_env == "development",
)

async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with async_session_maker() as session:
        yield session
