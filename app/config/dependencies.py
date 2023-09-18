from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_async_session
from app.modules.todo.infrastructure.repository import SQLToDoRepository
from app.modules.todo.application.service import ToDoService

def get_repository_todo(session: AsyncSession = Depends(get_async_session)):
    return SQLToDoRepository(session)

def get_service_todo(repo: SQLToDoRepository = Depends(get_repository_todo)):
    return ToDoService(repo)