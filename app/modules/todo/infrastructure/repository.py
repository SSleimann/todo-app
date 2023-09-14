from app.kernel.infrastructure.repository import SQLAlchemyRepository
from app.modules.todo.domain.repository import ToDoRepository
from app.modules.todo.infrastructure.mapper import TaskMapper
from app.modules.todo.infrastructure.models import TaskModel

class SQLToDoRepository(ToDoRepository, SQLAlchemyRepository):
    mapper_class = TaskMapper
    model_class = TaskModel
    
