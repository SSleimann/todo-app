import pytest

from fastapi.testclient import TestClient

from app.kernel.domain.exceptions import EntityNotFoundException
from app.modules.todo.infrastructure.repository import SQLToDoRepository
from app.modules.todo.domain.entities import TaskEntity
from app.modules.todo.domain.value_objects import StatusValue


def test_create_route_todo(api_client: TestClient, user_test):
    payload = {"title": "hola", "description": "a", "status": 3}
    headers = {"Authorization": f"Bearer {user_test.access_token}"}
    
    req = api_client.post("/todo/create", json=payload, headers=headers)
    json = req.json()

    assert req.status_code == 201
    assert json["data"].pop("id") is not None
    assert json["data"].pop("user_id") == str(user_test.id)
    assert payload == json["data"]


async def test_get_router_todo(api_client: TestClient, task_test):
    headers = {"Authorization": f"Bearer {task_test.user.access_token}"}
    req = api_client.get(f"/todo/{str(task_test.id)}", headers=headers)
    json = req.json()

    assert json["data"]["id"] == str(task_test.id)
    assert json["data"]["title"] == task_test.title
    assert json["data"]["status"] == task_test.status.value
    assert json["data"]["user_id"] == str(task_test.user_id)
    assert req.status_code == 200


async def test_delete_router_todo(api_client: TestClient, session, user_test):
    repo = SQLToDoRepository(session)
    headers = {"Authorization": f"Bearer {user_test.access_token}"}
    taskCreated = await repo.create(
        TaskEntity(
            id=TaskEntity.next_id(),
            title="Test Title",
            description="Test Description",
            status=StatusValue.PENDING,
            user_id=user_test.id,
        )
    )

    req = api_client.delete(f"/todo/{taskCreated.id}", headers=headers)
    json = req.json()

    assert json["data"]["id"] == str(taskCreated.id)
    assert json["data"]["title"] == taskCreated.title
    assert json["data"]["status"] == taskCreated.status.value
    assert json["data"]["user_id"] == str(taskCreated.user_id)
    assert req.status_code == 200

    with pytest.raises(EntityNotFoundException):
        await repo.get(taskCreated.id)


def test_get_all_paginated_router_without_query(api_client: TestClient, task_test):
    headers = {"Authorization": f"Bearer {task_test.user.access_token}"}
    
    req = api_client.get("/todo/", headers=headers)
    json = req.json()

    assert len(json["data"]) != 0
    assert json["message"].lower() == "ok!"


def test_get_all_paginated_router_per_page(api_client: TestClient, task_test):
    headers = {"Authorization": f"Bearer {task_test.user.access_token}"}
    req = api_client.get("/todo/", params={"per_page": 1}, headers=headers)
    json = req.json()

    assert len(json["data"]) == 1
    assert json["message"].lower() == "ok!"


def test_get_all_paginated_router_page(api_client: TestClient, task_test):
    headers = {"Authorization": f"Bearer {task_test.user.access_token}"}
    
    req = api_client.get("/todo/", params={"page": 2}, headers=headers)
    json = req.json()

    assert len(json["data"]) == 0
    assert json["message"].lower() == "ok!"


async def test_update_router_put(api_client: TestClient, session, task_test):
    repo = SQLToDoRepository(session)
    headers = {"Authorization": f"Bearer {task_test.user.access_token}"}
    taskGet = await repo.get_by_params(
        {
            "id": task_test.id,
            "user_id": task_test.user_id
        }
    )
    
    payload = {
        "id": str(taskGet.id),
        "title": "test title 2",
        "description": "Test Description 2",
        "status": 1,
    }

    req = api_client.put("/todo/update", json=payload, headers=headers)
    json = req.json()
    
    assert json["data"]["id"] == str(taskGet.id)
    assert json["data"]["title"] != taskGet.title
    assert json["data"]["description"] != taskGet.description
    assert json["data"]["status"] != taskGet.status.value
    assert json["data"]["user_id"] == str(task_test.user_id)
    assert json["data"]["title"] == task_test.title
    assert req.status_code == 200
    


async def test_update_router_patch(api_client: TestClient, session, task_test):
    repo = SQLToDoRepository(session)
    headers = {"Authorization": f"Bearer {task_test.user.access_token}"}
    taskGet = await repo.get_by_params(
        {
            "id": task_test.id,
            "user_id": task_test.user_id
        }
    )
    payload = {"id": str(taskGet.id), "status": 1}

    req = api_client.patch("/todo/update", json=payload, headers=headers)
    json = req.json()
    
    assert json["data"]["id"] == str(taskGet.id)
    assert json["data"]["title"] == taskGet.title
    assert json["data"]["description"] == taskGet.description
    assert json["data"]["status"] != taskGet.status.value
    assert json["data"]["user_id"] == str(taskGet.user_id)
    assert json["data"]["title"] == task_test.title
    assert req.status_code == 200
