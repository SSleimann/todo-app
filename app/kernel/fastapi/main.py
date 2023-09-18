from fastapi import FastAPI, Depends

from app.kernel.fastapi.error_handlers import init_error_handlers
from app.kernel.fastapi.routes import add_multiple_routes
from app.modules.todo.application.routes import todo_router

app = FastAPI()

init_error_handlers(app)
add_multiple_routes(app, [todo_router])


