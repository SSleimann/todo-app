from fastapi import Depends, APIRouter

from pydantic import UUID4

from app.config.dependencies import get_service_user
from app.kernel.application.response import Response
from app.modules.user.application.dto import UserCreationDTO, UserDTO, LoginDTO
from app.modules.user.application.service import UserService

user_router = APIRouter(prefix="/user")

@user_router.post("/register", response_model=Response[UserDTO], status_code=201)
async def register_user(body: UserCreationDTO, service: UserService = Depends(get_service_user)):
    result = await service.create(body)

    return result

@user_router.post('/login', response_model=Response[UserDTO])
async def login_user(body: LoginDTO, service: UserService = Depends(get_service_user)):
    result = await service.login(body)
    
    return result