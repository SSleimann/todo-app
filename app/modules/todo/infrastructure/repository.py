from app.kernel.domain.value_objects import ValueUUID
from app.kernel.domain.exceptions import EntityNotFoundException
from app.kernel.infrastructure.repository import SQLAlchemyRepository
from app.modules.todo.domain.entities import TaskEntity
from app.modules.todo.domain.repository import ToDoRepository
from app.modules.todo.domain.value_objects import StatusValue
from app.modules.todo.infrastructure.mapper import TaskMapper
from app.modules.todo.infrastructure.models import TaskModel

class SQLToDoRepository(ToDoRepository, SQLAlchemyRepository):
    mapper_class = TaskMapper
    model_class = TaskModel
    
    
    async def set_status_value(self, task_id: ValueUUID, status: StatusValue) -> TaskEntity:
        model = self.get_model_class()
        instance = await self._session.get(model, task_id)
        
        if instance is None:
            raise EntityNotFoundException
        
        instance.status = status
        
        await self._session.commit()
        
        return self.model_to_entity(instance)
    

