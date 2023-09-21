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
    