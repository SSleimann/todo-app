from abc import ABC, abstractmethod

from app.kernel.domain.repository import BaseRepository
from app.kernel.domain.value_objects import ValueUUID
from app.modules.todo.domain.entities import TaskEntity
from app.modules.todo.domain.value_objects import StatusValue

class ToDoRepository(BaseRepository, ABC):
    """ Interface for ToDo repository """
    
    @abstractmethod
    async def set_status_value(self, task_id: ValueUUID, status: StatusValue) -> TaskEntity:
        ...