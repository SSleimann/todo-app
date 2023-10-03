from uuid import UUID

from app.modules.todo.domain.entities import TaskEntity
from app.kernel.domain.service import BaseService
from app.modules.todo.application.dto import (
    TaskCreationDTO,
    TaskDTO,
    TaskUpdatePatchDTO,
    TaskUpdatePutDTO,
)


class ToDoService(BaseService):
    async def create(self, user_id, taskDto: TaskCreationDTO) -> dict[str, TaskDTO]:
        task_entity = TaskEntity(
            id=TaskEntity.next_id(),
            title=taskDto.title,
            description=taskDto.description,
            status=taskDto.status,
            user_id=user_id,
        )
        result = await self.repository.create(task_entity)

        dto = TaskDTO(
            id=result.id,
            title=result.title,
            description=result.description,
            status=result.status,
            user_id=result.user_id,
        )

        return {"message": "Created!", "data": dto}

    async def delete(self, task_id: UUID, user_id: UUID) -> dict[str, TaskDTO]:
        task = await self.repository.get_by_params(
            {"id": task_id, "user_id": user_id}
        )
        
        result = await self.repository.delete(task.id)

        dto = TaskDTO(
            id=result.id,
            title=result.title,
            description=result.description,
            status=result.status,
            user_id=result.user_id,
        )

        return {"message": "Deleted!", "data": dto}

    async def get_by_params(self, task_id: UUID, user_id: UUID) -> dict[str, TaskDTO]:
        result = await self.repository.get_by_params(
            {"id": task_id, "user_id": user_id}
        )

        dto = TaskDTO(
            id=result.id,
            title=result.title,
            description=result.description,
            status=result.status,
            user_id=result.user_id,
        )

        return {"message": "Ok!", "data": dto}

    async def update(
        self, task_id: UUID, user_id: UUID, taskDto: TaskUpdatePutDTO | TaskUpdatePatchDTO
    ) -> dict[str, TaskDTO]:
        task = await self.repository.get_by_params({"id": task_id, "user_id": user_id})

        result = await self.repository.update(
            task.id, taskDto.model_dump(exclude_none=True)
        )

        dto = TaskDTO(
            id=result.id,
            title=result.title,
            description=result.description,
            status=result.status,
            user_id=result.user_id,
        )

        return {"message": "Updated!", "data": dto}

    async def get_all_paginated_params(
        self, user_id: UUID, page: int = 1, per_page: int = 10
    ) -> dict[str, list[TaskDTO]]:
        results = await self.repository.get_all_paginated_with_params(
            {"user_id": user_id}, page, per_page
        )

        instances = [
            TaskDTO(
                id=obj.id,
                title=obj.title,
                description=obj.description,
                status=obj.status,
                user_id=obj.user_id,
            )
            for obj in results
        ]

        return {"message": "Ok!", "data": instances}
