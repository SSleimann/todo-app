from fastapi import Depends, APIRouter

from app.config.apiconfig import mem_cache

from app.config.dependencies import get_service_user, get_current_active_user, get_service_usercache, get_current_user
from app.kernel.application.response import Response
from app.modules.user.application.dto import (
    UserCreationDTO,
    UserDTO,
    LoginDTO,
    TokenDTO,
    UserCodeDTO
)
from app.modules.user.application.service import UserService, UserCacheService

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/register", response_model=Response[UserDTO], status_code=201)
async def register_user(
    body: UserCreationDTO, service: UserService = Depends(get_service_user)
):
    result = await service.create(body)

    return result

@user_router.get("/activate", response_model=Response[UserCodeDTO], status_code=200)
async def activate(
    current_user: UserDTO = Depends(get_current_user),
    service: UserCacheService = Depends(get_service_usercache)
):
    result = await service.get_code_for_activation(current_user.id)
    
    return {"message": f"You can activate your account", "data":result}

@user_router.get("/activate/{code}", response_model=Response[UserDTO], status_code=200)
async def activate(
    code: str,
    current_user: UserDTO = Depends(get_current_user),
    service: UserCacheService = Depends(get_service_usercache)
):
    code = code.encode()
    result = await service.activate_account(current_user.id, code)
    
    return {"message": "Active!", "data": result}

@user_router.post("/login", response_model=Response[TokenDTO])
async def login_user(body: LoginDTO, service: UserService = Depends(get_service_user)):
    result = await service.login(body)

    return result


@user_router.get("/me", response_model=Response[UserDTO])
async def get_user_me(
    current_user: UserDTO = Depends(get_current_active_user),
    service: UserService = Depends(get_service_user),
):
    result = await service.get(current_user.id)

    return result
