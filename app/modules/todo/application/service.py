from app.modules.todo.domain.entities import TaskEntity
from app.modules.todo.domain.service import ToDoServiceInterface
from app.modules.todo.application.dto import TaskCreationDTO, TaskDeletionDTO, TaskGetDTO, TaskUpdateDTO


class ToDoService(ToDoServiceInterface):
    async def create(self, taskDto: TaskCreationDTO) -> TaskEntity:
        task_entity = TaskEntity(
            id=TaskEntity.next_id(),
            title=taskDto.title,
            description=taskDto.description,
            status=taskDto.status,
        )
        result = await self.repository.create(task_entity)
        return result

    async def delete(self, taskDto: TaskDeletionDTO) -> TaskEntity:
        result = await self.repository.delete(taskDto.id)
        return result
    
    async def get(self, taskDto: TaskGetDTO) -> TaskEntity:
        result = await self.repository.get(taskDto)
        return result
    
    async def get_all(self) -> list[TaskEntity]:
        return await self.repository.get_all()
    
    async def update(self, taskDto: TaskUpdateDTO) -> TaskEntity:
        task_entity = TaskEntity(
            id=taskDto.id,
            title=taskDto.title,
            description=taskDto.description,
            status=taskDto.status
        )
        return await self.repository.update(task_entity)
        