from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.kernel.domain.exceptions import EntityNotFoundException

def init_error_handlers(app: FastAPI):
    @app.exception_handler(EntityNotFoundException)
    def exception_entity_handler(req: Request, exec: EntityNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"message":  exec.message}
        )
    
