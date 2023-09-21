import pytest

from app.modules.todo.infrastructure.models import TaskModel
from app.modules.todo.domain.value_objects import StatusValue
from app.modules.todo.application.dto import (
    TaskCreationDTO,
    TaskDeletionDTO,
    TaskGetDTO,
    TaskUpdatePutDTO,
    TaskUpdatePatchDTO
)
from app.modules.todo.application.service import ToDoService
from app.modules.todo.infrastructure.repository import SQLToDoRepository

pytestmark = pytest.mark.anyio


async def test_service_task_create(session):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    task_creation_dto = TaskCreationDTO(title="test", description="test")
    result = await service.create(task_creation_dto)

    assert result['data'].title == task_creation_dto.title
    assert result['data'].description == task_creation_dto.description
    assert result['data'].id is not None
    assert result['data'].status == StatusValue.PENDING


async def test_service_task_get(session):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    task_creation_dto = TaskCreationDTO(title="test", description="test")
    newEntity = await service.create(task_creation_dto)
    entity_id_dto = TaskGetDTO(id=newEntity['data'].id)
    
    result = await service.get(entity_id_dto)

    assert result['data'].title == task_creation_dto.title
    assert result['data'].id == entity_id_dto.id


async def test_service_get_all(session):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    result = await service.get_all()

    assert result['data'] is not None
    assert len(result['data']) != 0


async def test_service_task_delete(session):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    task_creation_dto = TaskCreationDTO(title="test", description="test")
    newEntity = await service.create(task_creation_dto)
    entity_id_delete_dto = TaskDeletionDTO(id=newEntity['data'].id)

    result = await service.delete(entity_id_delete_dto)
    find = await session.get(TaskModel, result['data'].id)

    assert result['data'].id == entity_id_delete_dto.id
    assert find is None


async def test_update_put_task(session):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    task_creation_dto = TaskCreationDTO(title="test", description="test")
    newEntity = await service.create(task_creation_dto)
    entity_update_dto = TaskUpdatePutDTO(
        id=newEntity['data'].id, title="test2", description="test2", status=StatusValue.CANCELLED
    )

    result = await service.update(entity_update_dto)

    assert result['data'].id == entity_update_dto.id
    assert result['data'].title == entity_update_dto.title
    assert result['data'].description == entity_update_dto.description
    assert result['data'].title != newEntity['data'].title
    assert result['data'].status == entity_update_dto.status

async def test_update_patch_task(session):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    task_creation_dto = TaskCreationDTO(title="test", description="test")
    newEntity = await service.create(task_creation_dto)
    entity_update_dto = TaskUpdatePatchDTO(
        id=newEntity['data'].id, title="test2"
    )

    result = await service.update(entity_update_dto)

    assert result['data'].id == entity_update_dto.id
    assert result['data'].title == entity_update_dto.title
    assert result['data'].description != entity_update_dto.description
    assert result['data'].title != newEntity['data'].title

async def test_get_all_paginated(session):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)
    
    result = await service.get_all_paginated()
    
    assert len(result['data']) > 0 and len(result['data']) <= 10