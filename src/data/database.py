from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config.config import config

# Database Engine Initialization
async_engine = create_async_engine(
    config.DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30
)

# Database Session Factory
AsyncSessionFactory = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency Function
async def fetch_db_session() -> AsyncGenerator[AsyncSession, None]:
    db_session = AsyncSessionFactory()
    try:
        yield db_session
    finally:
        await db_session.close()
