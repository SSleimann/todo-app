import uuid

from anyio import get_current_task

from sqlalchemy.ext.asyncio import create_async_engine, async_scoped_session, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID

from typing import AsyncGenerator

from app.config.apiconfig import current_config

class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value

Base = declarative_base()
engine = create_async_engine(current_config.database_url, echo=True, future=True)
session_factory = async_scoped_session(
    sessionmaker(
        autoflush=False, 
        autocommit=False, 
        bind=engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    ),
    scopefunc=get_current_task
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    session = session_factory()
    
    try:
        yield session
    except:
        await session.rollback()
    finally:
        await session.close()
    

