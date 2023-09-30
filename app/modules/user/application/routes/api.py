from fastapi import Depends, APIRouter

from app.config.dependencies import get_service_user, get_current_active_user
from app.kernel.application.response import Response
from app.modules.user.application.dto import (
    UserCreationDTO,
    UserDTO,
    LoginDTO,
    TokenDTO,
    UserGetDTO,
)
from app.modules.user.application.service import UserService

user_router = APIRouter(prefix="/user")


@user_router.post("/register", response_model=Response[UserDTO], status_code=201)
async def register_user(
    body: UserCreationDTO, service: UserService = Depends(get_service_user)
):
    result = await service.create(body)

    return result


@user_router.post("/login", response_model=Response[TokenDTO])
async def login_user(body: LoginDTO, service: UserService = Depends(get_service_user)):
    result = await service.login(body)

    return result


@user_router.get("/me", response_model=Response[UserDTO])
async def get_user_me(
    current_user: UserDTO = Depends(get_current_active_user),
    service: UserService = Depends(get_service_user),
):
    dto = UserGetDTO(id=current_user.id)
    result = await service.get(dto)

    return result
