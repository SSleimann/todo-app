from app.modules.todo.domain.entities import TaskEntity
from app.kernel.domain.service import BaseService
from app.modules.todo.application.dto import (
    TaskCreationDTO,
    TaskDeletionDTO,
    TaskGetDTO,
    TaskDTO,
    TaskUpdatePatchDTO,
    TaskUpdatePutDTO,
)


class ToDoService(BaseService):
    async def create(self, taskDto: TaskCreationDTO) -> dict[str, TaskDTO]:
        task_entity = TaskEntity(
            id=TaskEntity.next_id(),
            title=taskDto.title,
            description=taskDto.description,
            status=taskDto.status,
        )
        result = await self.repository.create(task_entity)

        dto = TaskDTO(
            id=result.id,
            title=result.title,
            description=result.description,
            status=result.status,
        )

        return {"message": "Created!", "data": dto}

    async def delete(self, taskDto: TaskDeletionDTO) -> dict[str, TaskDTO]:
        result = await self.repository.delete(taskDto.id)

        dto = TaskDTO(
            id=result.id,
            title=result.title,
            description=result.description,
            status=result.status,
        )

        return {"message": "Deleted!", "data": dto}

    async def get(self, taskDto: TaskGetDTO) -> dict[str, TaskDTO]:
        result = await self.repository.get(taskDto.id)

        dto = TaskDTO(
            id=result.id,
            title=result.title,
            description=result.description,
            status=result.status,
        )

        return {"message": "Ok!", "data": dto}

    async def get_all(self) -> dict[str, list[TaskDTO]]:
        results = await self.repository.get_all()
        instances = [
            TaskDTO(
                id=obj.id,
                title=obj.title,
                description=obj.description,
                status=obj.status,
            )
            for obj in results
        ]

        return {"message": "Ok!", "data": instances}

    async def update(
        self, taskDto: TaskUpdatePutDTO | TaskUpdatePatchDTO
    ) -> dict[str, TaskDTO]:
        result = await self.repository.update(taskDto.id, taskDto.model_dump(exclude_none=True, exclude={'id'}))

        dto = TaskDTO(
            id=result.id,
            title=result.title,
            description=result.description,
            status=result.status,
        )

        return {"message": "Updated!", "data": dto}

    async def get_all_paginated(
        self, page: int = 1, per_page: int = 10
    ) -> dict[str, list[TaskDTO]]:
        results = await self.repository.get_paginated_all(page, per_page)

        instances = [
            TaskDTO(
                id=obj.id,
                title=obj.title,
                description=obj.description,
                status=obj.status,
            )
            for obj in results
        ]

        return {"message": "Ok!", "data": instances}
