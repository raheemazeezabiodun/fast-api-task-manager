import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from sqlmodel import SQLModel
from main import app
from deep_medical import settings




@pytest.fixture(scope="function", autouse=True)
async def db_engine(postgresql):
    connection = f'postgresql+asyncpg://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}'
    settings.DATABASE_URL = connection
    engine = create_async_engine(connection, echo=True)
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    # Drop all tables after tests are done
    async with engine.begin() as conn:
        for table in SQLModel.metadata.sorted_tables:
            await conn.execute(table.delete())
            await conn.commit()

@pytest.fixture(scope="function", autouse=True)
def db_session(db_engine):
    """Create a session for testing"""
    SessionLocal = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    session = SessionLocal()
    yield session
    # Cleanup
    session.close()


@pytest.fixture(autouse=True)
def client(db_engine):
    client = TestClient(app)
    yield client
