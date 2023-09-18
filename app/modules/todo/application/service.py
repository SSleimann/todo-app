from app.modules.todo.domain.entities import TaskEntity
from app.kernel.domain.service import BaseService
from app.modules.todo.application.dto import TaskCreationDTO, TaskDeletionDTO, TaskGetDTO, TaskUpdateDTO, TaskSetStatusValueDTO, TaskDTO

class ToDoService(BaseService):
    async def create(self, taskDto: TaskCreationDTO) -> TaskDTO:
        task_entity = TaskEntity(
            id=TaskEntity.next_id(),
            title=taskDto.title,
            description=taskDto.description,
            status=taskDto.status,
        )
        result = await self.repository.create(task_entity)
        return TaskDTO(
            id=result.id,
            title=result.title,
            description=result.description,
            status=result.status
        )

    async def delete(self, taskDto: TaskDeletionDTO) -> TaskEntity:
        result = await self.repository.delete(taskDto.id)
        return result
    
    async def get(self, taskDto: TaskGetDTO) -> TaskEntity:
        result = await self.repository.get(taskDto.id)
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
        
    async def set_status_value(self, taskDto: TaskSetStatusValueDTO) -> TaskEntity:
        return await self.repository.set_status_value(taskDto.id, taskDto.status)
    
