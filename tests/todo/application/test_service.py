import pytest

from app.modules.todo.infrastructure.models import TaskModel
from app.modules.todo.domain.value_objects import StatusValue
from app.modules.todo.application.dto import (
    TaskCreationDTO,
    TaskDeletionDTO,
    TaskGetParamsDTO,
    TaskUpdatePutDTO,
    TaskUpdatePatchDTO,
    TaskGetAllParams
)
from app.modules.todo.application.service import ToDoService
from app.modules.todo.infrastructure.repository import SQLToDoRepository
from app.kernel.domain.value_objects import ValueUUID

pytestmark = pytest.mark.anyio


async def test_service_task_create(session, user_test):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    task_creation_dto = TaskCreationDTO(title="test", description="test", user_id=user_test.id)
    result = await service.create(task_creation_dto)

    assert result["data"].title == task_creation_dto.title
    assert result["data"].description == task_creation_dto.description
    assert result["data"].id is not None
    assert result["data"].status == StatusValue.PENDING
    assert result["data"].user_id == user_test.id


async def test_service_task_get(session, task_test):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    entity_id_dto = TaskGetParamsDTO(id=task_test.id, user_id=task_test.user_id)

    result = await service.get_by_params(entity_id_dto)

    assert result["data"].title == task_test.title
    assert result["data"].id == task_test.id
    assert result["data"].status == task_test.status
    assert result["data"].user_id == task_test.user.id

async def test_service_task_delete(session, user_test):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    task_creation_dto = TaskCreationDTO(title="test", description="test", user_id=user_test.id)
    newEntity = await service.create(task_creation_dto)
    entity_id_delete_dto = TaskDeletionDTO(id=newEntity["data"].id, user_id=user_test.id)

    result = await service.delete(entity_id_delete_dto)
    find = await session.get(TaskModel, result["data"].id)

    assert result["data"].id == entity_id_delete_dto.id
    assert find is None
    assert result["data"].user_id == user_test.id


async def test_update_put_task(session, task_test):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)
    
    last_title = task_test.title
    
    entity_update_dto = TaskUpdatePutDTO(
        id=task_test.id,
        user_id=task_test.user_id,
        title="test2",
        description="test2",
        status=StatusValue.CANCELLED,
    )

    result = await service.update(entity_update_dto)

    assert result["data"].id == entity_update_dto.id
    assert result["data"].title == entity_update_dto.title
    assert result["data"].description == entity_update_dto.description
    assert result["data"].title != last_title
    assert result["data"].status == entity_update_dto.status
    assert result["data"].user_id == task_test.user_id


async def test_update_patch_task(session, task_test):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    last_title =task_test.title

    entity_update_dto = TaskUpdatePatchDTO(id=task_test.id, user_id=task_test.user_id, title="test2")

    result = await service.update(entity_update_dto)

    assert result["data"].id == entity_update_dto.id
    assert result["data"].title == entity_update_dto.title
    assert result["data"].description != entity_update_dto.description
    assert result["data"].title != last_title
    assert result["data"].user_id == task_test.user_id


async def test_get_all_paginated(session, task_test):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)
    
    dto= TaskGetAllParams(user_id=task_test.user_id)

    result = await service.get_all_paginated_params(dto)
    
    assert len(result["data"]) > 0 and len(result["data"]) <= 10
    assert result["data"][0].title == task_test.title
    assert result["data"][0].user_id == task_test.user_id
