import pytest

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.config.apiconfig import TestSettings
from app.config.database import Base

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
async def db(anyio_backend):
    settings = TestSettings()
    engine = create_async_engine(settings.database_url, future=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    return engine

@pytest.fixture(scope="function")
async def session(db):
    async with AsyncSession(db, expire_on_commit=False) as session:
        yield session
        
    