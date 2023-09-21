from typing import Annotated

from fastapi import Depends, APIRouter, Query

from app.config.dependencies import get_service_todo
from app.modules.todo.application.dto import TaskCreationDTO, TaskGetDTO, TaskDeletionDTO, TaskDTO, TaskUpdatePatchDTO, TaskUpdatePutDTO
from app.modules.todo.application.service import ToDoService
from app.kernel.application.response import Response

todo_router = APIRouter(prefix='/todo')

@todo_router.post('/create', status_code=201, response_model=Response[TaskDTO])
async def create_task_todo(body: TaskCreationDTO, service: ToDoService = Depends(get_service_todo)):
    result = await service.create(body)
    
    return result

@todo_router.get('/{uuid}', status_code=200, response_model=Response[TaskDTO])
async def get_task(uuid: str, service: ToDoService = Depends(get_service_todo)):
    dto = TaskGetDTO(id=uuid)
    result = await service.get(dto)
    
    return result

@todo_router.delete('/{uuid}', status_code=200, response_model=Response[TaskDTO])
async def get_task(uuid: str, service: ToDoService = Depends(get_service_todo)):
    dto = TaskDeletionDTO(id=uuid)
    result = await service.delete(dto)
    
    return result

@todo_router.get('/', status_code=202, response_model=Response[TaskDTO])
async def get_all_task_paginated(
    page: Annotated[ int, Query(ge=1) ] = 1,
    per_page: Annotated[ int, Query(ge=0) ] = 10,
    service: ToDoService = Depends(get_service_todo)
    ):
    result = await service.get_all_paginated(page=page, per_page=per_page)
    
    return result


@todo_router.put('/update', status_code=200, response_model=Response[TaskDTO])
async def update_put(body: TaskUpdatePutDTO, service: ToDoService = Depends(get_service_todo)):
    result = await service.update(body)
    
    return result
    
    
@todo_router.patch('/update', status_code=200, response_model=Response[TaskDTO])
async def update_patch(body: TaskUpdatePatchDTO, service: ToDoService = Depends(get_service_todo)):
    result = await service.update(body)
    
    return result