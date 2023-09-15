import pytest

from app.modules.todo.infrastructure.models import TaskModel
from app.modules.todo.domain.value_objects import StatusValue
from app.modules.todo.application.dto import (
    TaskCreationDTO,
    TaskDeletionDTO,
    TaskGetDTO,
    TaskSetStatusValueDTO,
    TaskUpdateDTO,
)
from app.modules.todo.application.service import ToDoService
from app.modules.todo.infrastructure.repository import SQLToDoRepository

pytestmark = pytest.mark.anyio


async def test_service_task_create(session):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    task_creation_dto = TaskCreationDTO(title="test", description="test")
    result = await service.create(task_creation_dto)

    assert result.title == task_creation_dto.title
    assert result.description == task_creation_dto.description
    assert result.id is not None
    assert result.status == StatusValue.PENDING


async def test_service_task_get(session):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    task_creation_dto = TaskCreationDTO(title="test", description="test")
    newEntity = await service.create(task_creation_dto)
    entity_id_dto = TaskGetDTO(id=newEntity.id)

    result = await service.get(entity_id_dto)

    assert result.title == task_creation_dto.title
    assert result.id == entity_id_dto.id


async def test_service_get_all(session):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    result = await service.get_all()

    assert result is not None
    assert len(result) != 0


async def test_service_task_delete(session):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    task_creation_dto = TaskCreationDTO(title="test", description="test")
    newEntity = await service.create(task_creation_dto)
    entity_id_delete_dto = TaskDeletionDTO(id=newEntity.id)

    result = await service.delete(entity_id_delete_dto)
    find = await session.get(TaskModel, result.id)

    assert result.id == entity_id_delete_dto.id
    assert find is None


async def test_set_status_value(session):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    task_creation_dto = TaskCreationDTO(title="test", description="test")
    newEntity = await service.create(task_creation_dto)
    entity_set_status_dto = TaskSetStatusValueDTO(
        id=newEntity.id, status=StatusValue.DONE
    )

    result = await service.set_status_value(entity_set_status_dto)

    assert result.id == entity_set_status_dto.id
    assert result.status == entity_set_status_dto.status


async def test_update_task(session):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    task_creation_dto = TaskCreationDTO(title="test", description="test")
    newEntity = await service.create(task_creation_dto)
    entity_update_dto = TaskUpdateDTO(
        id=newEntity.id, title="test2", description="test2"
    )

    result = await service.update(entity_update_dto)

    assert result.id == entity_update_dto.id
    assert result.title == entity_update_dto.title
    assert result.description == entity_update_dto.description
    assert result.title != newEntity.title
