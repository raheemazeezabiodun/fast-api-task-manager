from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from deep_medical import settings


_db_engines: Dict[str, AsyncEngine] = {}


def get_or_create_engine() -> AsyncEngine:
    key = url or settings.DATABASE_URL
    if key not in _db_engines:
        options = {
            "echo": True,
            "future": True,
            "poolclass": NullPool,
        }
        engine = create_async_engine(settings.DATABASE_URL, **options)
        _db_engines[key] = engine

    return _db_engines[key]


def get_session() -> AsyncSession:
    engine = get_or_create_engine()

    async_session = async_sessionmaker(engine, expire_on_commit=True)
    return async_session()


@asynccontextmanager
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    session = get_session()
    try:
        yield session
    finally:
        await session.close()
