import pytest
import enum

from app.kernel.domain.exceptions import EntityNotFoundException
from app.modules.todo.infrastructure.repository import SQLToDoRepository
from app.modules.todo.domain.entities import TaskEntity
from app.modules.todo.domain.value_objects import StatusValue

pytestmark = pytest.mark.anyio

async def test_set_status_value(session):
    repo = SQLToDoRepository(session)
    
    taskCreated = await repo.create(
        TaskEntity(
            id=TaskEntity.next_id(),
            title='Test Title',
            description='Test Description',
            status=StatusValue.PENDING
        )
    )
    
    result = await repo.set_status_value(task_id=taskCreated.id, status=StatusValue.DONE)
    
    assert result.id == taskCreated.id
    assert result.title == taskCreated.title
    assert result.status != taskCreated.status
    

async def test_set_status_value_not_found(session):
    repo = SQLToDoRepository(session)
    
    with pytest.raises(EntityNotFoundException):
        await repo.set_status_value(task_id=TaskEntity.next_id(), status=StatusValue.DONE)