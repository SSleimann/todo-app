from uuid import UUID
from datetime import datetime, timedelta

from app.config.security import gen_hashed_password, verify_password, decode_jwt, generate_code

from app.config.apiconfig import current_config
from app.kernel.domain.service import BaseService
from app.kernel.domain.exceptions import EntityNotFoundException, AuthErrorException
from app.modules.user.domain.entities import UserEntity
from app.modules.user.domain.value_objects import Email
from app.modules.cache.application.service import CacheService
from app.modules.user.domain.exceptions import CodeActivationExists
from app.modules.cache.domain.entities import CacheDataEntity
from app.modules.cache.application.dto import CacheDataDTO, AddToCacheDTO

from app.modules.user.application.dto import (
    TokenDTO,
    LoginDTO,
    UserCreationDTO,
    UserDTO,
    UserCodeDTO
)


class UserService(BaseService):
    async def create(self, dto: UserCreationDTO) -> dict[str, UserDTO]:
        paswd = dto.password.get_secret_value()
        hashed = gen_hashed_password(paswd)

        entity = UserEntity(
            id=UserEntity.next_id(),
            email=Email(dto.email),
            password=hashed,
            access_token=None,
            username=dto.username,
            is_active=False,
        )

        instance = await self.repository.create(entity)

        dto = UserDTO(
            id=instance.id,
            email=instance.email,
            username=instance.username,
            access_token=instance.access_token,
            is_active=instance.is_active,
            task_count=instance.task_count
        )

        return {"message": "Created!", "data": dto}

    async def get(self, user_id: UUID) -> dict[str, UserDTO]:
        instance = await self.repository.get(user_id)

        dto = UserDTO(
            id=instance.id,
            email=instance.email,
            access_token=instance.access_token,
            username=instance.username,
            is_active=instance.is_active,
            task_count=instance.task_count
        )

        return {"message": "Ok!", "data": dto}

    async def login(self, dto: LoginDTO) -> dict[str, TokenDTO]:
        paswd = dto.password.get_secret_value()

        try:
            instance = await self.repository.get_by_email(Email(dto.email))
        except EntityNotFoundException:
            raise AuthErrorException("Invalid password or email!")

        if not verify_password(paswd, instance.password):
            raise AuthErrorException("Invalid password or email!")

        if decode_jwt(instance.access_token, current_config.jwt_secret_key) is None:
            instance = await self.repository.set_access_token(instance.id)

        dto = TokenDTO(access_token=instance.access_token, token_type="bearer")

        return {"message": "Authenticated!", "data": dto}

    async def get_by_email(self, email: Email) -> dict[str, UserDTO]:
        instance = await self.repository.get_by_email(email)

        dto = UserDTO(
            id=instance.id,
            email=instance.email,
            access_token=instance.access_token,
            username=instance.username,
            is_active=instance.is_active,
            task_count=instance.task_count
        )

        return {"message": "Ok!", "data": dto}

    async def get_by_access_token(self, access_token: str) -> dict[str, UserDTO]:
        instance = await self.repository.get_by_access_token(access_token)

        dto = UserDTO(
            id=instance.id,
            email=instance.email,
            access_token=instance.access_token,
            username=instance.username,
            is_active=instance.is_active,
            task_count=instance.task_count
        )

        return {"message": "Ok!", "data": dto}
    
    async def activate_account(self, id: UUID) -> UserDTO:
        user = await self.repository.get(id)
        
        if user.is_active:
            raise AuthErrorException("User already activated!")
        
        #Activate account
        activated_user = await self.repository.activate_account(user.id)
        
        dto = UserDTO(
            id=activated_user.id,
            email=activated_user.email,
            access_token=activated_user.access_token,
            username=activated_user.username,
            is_active=activated_user.is_active,
            task_count=activated_user.task_count
        )
        
        return dto
    
class UserCacheService(BaseService):
    def __init__(self, cache_service: CacheService, user_service: UserService) -> None:
        self.cache_service = cache_service
        self.user_service = user_service
        
    async def get_code_for_activation(self, id: UUID) -> UserCodeDTO:
        user = await self.user_service.get(id)
        user_data  = user["data"]
        
        if user_data.is_active:
            raise AuthErrorException("User is active!")
        
        #Check if exists another code for activation
        try:
            cache_user = self.cache_service.get(user_data.id)

        except EntityNotFoundException:
            cache_user = None
        
        if cache_user:
            raise CodeActivationExists
        
        code = generate_code()
        entity = CacheDataEntity(user_data.id, code)
        dto = AddToCacheDTO(id=entity.id, data=entity.data)
        
        createdCodeEntity = self.cache_service.create(dto)
        exp_time = datetime.utcnow() + timedelta(seconds=current_config.mem_cache_expire_time_seconds)
        dto = UserCodeDTO(user_id=user_data.id, code=createdCodeEntity.data, expiration_time=exp_time)
        
        return dto
        
    async def activate_account(self, id: UUID, code: bytes) -> UserDTO:
        user = await self.user_service.get(id)
        user_data  = user["data"]
        
        if user_data.is_active:
            raise AuthErrorException("User already activated!")
        
        try:
            cache_user = self.cache_service.get(user_data.id)
        except EntityNotFoundException:
            raise AuthErrorException("Code invalid!")
        
        if cache_user.data != code:
            raise AuthErrorException("Code Invalid!")
        
        #Activate account
        activated_user = await self.user_service.activate_account(user_data.id)
        
        try:
            self.cache_service.delete(cache_user.id)
        except EntityNotFoundException:
            pass
        
        return activated_user