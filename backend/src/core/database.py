import orjson
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from . import settings

engine = create_async_engine(
    settings.db_url,
    echo=False,
    pool_size=20,           
    max_overflow=10,        
    pool_timeout=30,        
    pool_recycle=1800,
    pool_pre_ping=True,


    query_cache_size=1200,  # Cache für SQL-Kompilierung vergrössern

    json_serializer=lambda obj: orjson.dumps(obj).decode(),
    json_deserializer=orjson.loads,
)


async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False  
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an optimised asynchronous database session.

    The session is managed via a context manager to ensure that resources 
    are released and transactions are rolled back in case of failure. 
    Autoflush is disabled by default to reduce unnecessary database roundtrips.

    :yield: An instance of AsyncSession for database operations.
    :rtype: AsyncGenerator[AsyncSession, None]
    """
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
