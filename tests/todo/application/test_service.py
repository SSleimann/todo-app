import pytest

from app.modules.todo.infrastructure.models import TaskModel
from app.modules.todo.domain.value_objects import StatusValue
from app.modules.todo.application.dto import (
    TaskCreationDTO,
    TaskUpdatePutDTO,
    TaskUpdatePatchDTO,
)
from app.modules.todo.application.service import ToDoService
from app.modules.todo.infrastructure.repository import SQLToDoRepository
from app.kernel.domain.value_objects import ValueUUID

pytestmark = pytest.mark.anyio


async def test_service_task_create(session, user_test):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    task_creation_dto = TaskCreationDTO(
        title="test", description="test"
    )
    result = await service.create(user_test.id, task_creation_dto)

    assert result["data"].title == task_creation_dto.title
    assert result["data"].description == task_creation_dto.description
    assert result["data"].id is not None
    assert result["data"].status == StatusValue.PENDING
    assert result["data"].user_id == user_test.id


async def test_service_task_get(session, task_test):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    result = await service.get_by_params(task_test.id, task_test.user_id)

    assert result["data"].title == task_test.title
    assert result["data"].id == task_test.id
    assert result["data"].status == task_test.status
    assert result["data"].user_id == task_test.user_id


async def test_service_task_delete(session, user_test):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    task_creation_dto = TaskCreationDTO(
        title="test", description="test"
    )
    newEntity = await service.create(user_test.id, task_creation_dto)

    result = await service.delete(newEntity["data"].id, user_test.id)
    find = await session.get(TaskModel, result["data"].id)

    assert result["data"].id == newEntity["data"].id
    assert find is None
    assert result["data"].user_id == user_test.id


async def test_update_put_task(session, task_test):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    last_title = task_test.title

    entity_update_dto = TaskUpdatePutDTO(
        title="test2",
        description="test2",
        status=StatusValue.CANCELLED,
    )

    result = await service.update(task_test.id, task_test.user_id, entity_update_dto)

    assert result["data"].id == task_test.id
    assert result["data"].title == entity_update_dto.title
    assert result["data"].description == entity_update_dto.description
    assert result["data"].title != last_title
    assert result["data"].status == entity_update_dto.status
    assert result["data"].user_id == task_test.user_id


async def test_update_patch_task(session, task_test):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    last_title = task_test.title

    entity_update_dto = TaskUpdatePatchDTO(
        title="test2"
    )

    result = await service.update(task_test.id, task_test.user_id, entity_update_dto)

    assert result["data"].id == task_test.id
    assert result["data"].title == entity_update_dto.title
    assert result["data"].description != entity_update_dto.description
    assert result["data"].title != last_title
    assert result["data"].user_id == task_test.user_id


async def test_get_all_paginated(session, task_test):
    repo = SQLToDoRepository(session)
    service = ToDoService(repo)

    result = await service.get_all_paginated_params(task_test.user_id)

    assert len(result["data"]) > 0 and len(result["data"]) <= 10
    assert result["data"][0].title == task_test.title
    assert result["data"][0].user_id == task_test.user_id
