from fastapi import Depends

from app.config.dependencies import get_service_todo
from app.modules.todo.application.routes import todo_router
from app.modules.todo.application.dto import TaskDTO, TaskGetDTO
from app.modules.todo.application.service import ToDoService

@todo_router.post('/create', status_code=201, response_model=TaskDTO)
async def create_task_todo(body: TaskGetDTO, service: ToDoService = Depends(get_service_todo)):
    result = await service.create(body)
    
    return result