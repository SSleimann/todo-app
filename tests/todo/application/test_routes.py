import pytest

from fastapi.testclient import TestClient

from app.kernel.domain.exceptions import EntityNotFoundException
from app.modules.todo.infrastructure.repository import SQLToDoRepository
from app.modules.todo.domain.entities import TaskEntity
from app.modules.todo.domain.value_objects import StatusValue

def test_create_route_todo(api_client: TestClient):
    payload = {
        "title": "hola",
        "description": "a",
        "status": 3
    }
    
    req = api_client.post("/todo/create", json=payload)
    json = req.json()
    
    assert req.status_code == 201
    assert json['data']['id'] is not None
    json['data'].pop('id')
    assert payload == json['data']
    
async def test_get_router_todo(api_client: TestClient, session):
    repo = SQLToDoRepository(session)
    
    taskCreated = await repo.create(
        TaskEntity(
            id=TaskEntity.next_id(),
            title='Test Title',
            description='Test Description',
            status=StatusValue.PENDING
        )
    )
    
    req = api_client.get(f"/todo/{taskCreated.id}")
    json = req.json()
    
    assert json['data']['id'] == str(taskCreated.id)
    assert json['data']['title'] == taskCreated.title
    assert json['data']['status'] == taskCreated.status.value
    assert req.status_code == 200
    
async def test_delete_router_todo(api_client: TestClient, session):
    repo = SQLToDoRepository(session)
    
    taskCreated = await repo.create(
        TaskEntity(
            id=TaskEntity.next_id(),
            title='Test Title',
            description='Test Description',
            status=StatusValue.PENDING
        )
    )
    
    req = api_client.delete(f"/todo/{taskCreated.id}")
    json = req.json()
    
    assert json['data']['id'] == str(taskCreated.id)
    assert json['data']['title'] == taskCreated.title
    assert json['data']['status'] == taskCreated.status.value
    assert req.status_code == 200
    
    with pytest.raises(EntityNotFoundException):
        await repo.get(taskCreated.id)
    
def test_get_all_paginated_router_without_query(api_client: TestClient):
    req = api_client.get("/todo/")
    json = req.json()
    
    assert len(json['data']) != 0
    assert json['message'].lower() == 'ok!'

def test_get_all_paginated_router_per_page(api_client: TestClient):
    req = api_client.get("/todo/", params={"per_page": 3})
    json = req.json()
    
    assert len(json['data']) <= 3
    assert json['message'].lower() == 'ok!'

def test_get_all_paginated_router_page(api_client: TestClient):
    req = api_client.get("/todo/", params={"page": 2})
    json = req.json()
    
    assert len(json['data']) == 0
    assert json['message'].lower() == 'ok!'
    
async def test_update_router_put(api_client: TestClient, session):
    repo = SQLToDoRepository(session)
    
    taskCreated = await repo.create(
        TaskEntity(
            id=TaskEntity.next_id(),
            title='Test Title',
            description='Test Description',
            status=StatusValue.PENDING
        )
    )
    
    payload = {
        "id": str(taskCreated.id),
        "title": "test title 2",
        "description": 'Test Description 2',
        "status": 1
    }
    
    req = api_client.put("/todo/update", json=payload)
    json = req.json()
    
    assert json['data']['id'] == str(taskCreated.id)
    assert json['data']['title'] != taskCreated.title
    assert json['data']['description'] != taskCreated.description
    assert json['data']['status'] != taskCreated.status.value

async def test_update_router_patch(api_client: TestClient, session):
    repo = SQLToDoRepository(session)
    
    taskCreated = await repo.create(
        TaskEntity(
            id=TaskEntity.next_id(),
            title='Test Title',
            description='Test Description',
            status=StatusValue.PENDING
        )
    )
    
    payload = {
        "id": str(taskCreated.id),
        "status": 1
    }
    
    req = api_client.patch("/todo/update", json=payload)
    json = req.json()
    
    assert json['data']['id'] == str(taskCreated.id)
    assert json['data']['title'] == taskCreated.title
    assert json['data']['description'] == taskCreated.description
    assert json['data']['status'] != taskCreated.status.value