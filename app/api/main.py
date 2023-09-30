from fastapi import FastAPI, Depends

from app.api.error_handlers import init_error_handlers
from app.api.routes import add_multiple_routes
from app.modules.todo.application.routes.api import todo_router
from app.modules.user.application.routes.api import user_router

app = FastAPI()

init_error_handlers(app)
add_multiple_routes(app, [todo_router, user_router])
