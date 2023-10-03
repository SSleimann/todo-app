from typing import Annotated

from fastapi import Depends, APIRouter, Query
from pydantic import UUID4

from app.config.dependencies import get_service_todo, get_current_active_user
from app.modules.user.application.dto import UserDTO
from app.modules.todo.application.dto import (
    TaskCreationDTO,
    TaskGetParamsDTO,
    TaskDeletionDTO,
    TaskDTO,
    TaskUpdatePatchDTO,
    TaskUpdatePutDTO,
    TaskGetAllParams,
)
from app.modules.todo.application.service import ToDoService
from app.kernel.application.response import Response

todo_router = APIRouter(prefix="/todo", tags=["todo"])


@todo_router.post("/create", status_code=201, response_model=Response[TaskDTO])
async def create_task_todo(
    body: TaskCreationDTO,
    service: ToDoService = Depends(get_service_todo),
    user: UserDTO = Depends(get_current_active_user),
):
    body.user_id = user.id
    result = await service.create(body)

    return result


@todo_router.get("/{uuid}", status_code=200, response_model=Response[TaskDTO])
async def get_task(
    uuid: UUID4,
    service: ToDoService = Depends(get_service_todo),
    user: UserDTO = Depends(get_current_active_user),
):
    dto = TaskGetParamsDTO(id=uuid, user_id=user.id)
    result = await service.get_by_params(dto)

    return result


@todo_router.delete("/{uuid}", status_code=200, response_model=Response[TaskDTO])
async def get_task(
    uuid: UUID4,
    service: ToDoService = Depends(get_service_todo),
    user: UserDTO = Depends(get_current_active_user),
):
    dto = TaskDeletionDTO(id=uuid, user_id=user.id)
    result = await service.delete(dto)

    return result


@todo_router.get("/", status_code=202, response_model=Response[TaskDTO])
async def get_all_task_paginated(
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=0)] = 10,
    service: ToDoService = Depends(get_service_todo),
    user: UserDTO = Depends(get_current_active_user),
):
    dto = TaskGetAllParams(user_id=user.id)
    result = await service.get_all_paginated_params(dto, page=page, per_page=per_page)

    return result


@todo_router.put("/update", status_code=200, response_model=Response[TaskDTO])
async def update_put(
    body: TaskUpdatePutDTO,
    service: ToDoService = Depends(get_service_todo),
    user: UserDTO = Depends(get_current_active_user),
):
    body.user_id = user.id
    result = await service.update(body)

    return result


@todo_router.patch("/update", status_code=200, response_model=Response[TaskDTO])
async def update_patch(
    body: TaskUpdatePatchDTO,
    service: ToDoService = Depends(get_service_todo),
    user: UserDTO = Depends(get_current_active_user),
):
    body.user_id = user.id
    result = await service.update(body)

    return result
