from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode (helpful for learning!)
    future=True,
    pool_pre_ping=True,  # Verify connections are alive before using
    pool_size=5,  # Number of connections to keep open
    max_overflow=10,  # Max additional connections when pool is full
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit (important for async)
    autocommit=False,  # Explicitly commit (safer, more control)
    autoflush=False,  # Explicitly flush (prevents unexpected queries)
)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()