from typing import Annotated

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt, JWTError

from app.config.apiconfig import current_config
from app.config.database import get_async_session
from app.config.security import ALGORITHM, JWTBearer
from app.modules.todo.infrastructure.repository import SQLToDoRepository
from app.modules.todo.application.service import ToDoService
from app.modules.user.infrastructure.repository import UserRepository
from app.modules.user.application.service import UserService
from app.modules.user.application.dto import UserGetByEmailDTO, UserDTO
from app.kernel.domain.exceptions import AuthErrorException, EntityNotFoundException


def get_repository_todo(session: AsyncSession = Depends(get_async_session)):
    return SQLToDoRepository(session)


def get_service_todo(repo: SQLToDoRepository = Depends(get_repository_todo)):
    return ToDoService(repo)

def get_repository_user(session: AsyncSession = Depends(get_async_session)):
    return UserRepository(session)

def get_service_user(repo: UserRepository = Depends(get_repository_user)):
    return UserService(repo)

async def get_current_user(token: Annotated[str, Depends(JWTBearer())], service: UserService = Depends(get_service_user)):
    try:
        payload = jwt.decode(token, current_config.jwt_secret_key, algorithms=[ALGORITHM])
        email: str = payload.get("sub", None)
        dto = UserGetByEmailDTO(email=email)
        
        if email is None:
            raise AuthErrorException('Could not validate credentials!')
        
    except (JWTError) as e:
        print(e)
        raise AuthErrorException('Could not validate credentials!')
    
    try:
        current_user = await service.get_by_email(dto)
    except EntityNotFoundException:
        raise AuthErrorException('Invalid password or email!')
    
    return current_user['data']

async def get_current_active_user(current_user: UserDTO = Depends(get_current_user)):
    if not current_user.is_active:
        raise AuthErrorException('Inactive user!')
    
    return current_user
