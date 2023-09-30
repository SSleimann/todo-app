from app.config.security import gen_hashed_password, verify_password, decode_jwt

from app.config.apiconfig import current_config
from app.kernel.domain.service import BaseService
from app.kernel.domain.exceptions import EntityNotFoundException, AuthErrorException
from app.modules.user.domain.entities import UserEntity
from app.modules.user.domain.value_objects import Email
from app.modules.user.application.dto import (
    TokenDTO,
    LoginDTO,
    UserCreationDTO,
    UserDTO,
    UserGetByAccessTokenDTO,
    UserGetByEmailDTO,
    UserGetDTO,
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
            is_active=True,
        )

        instance = await self.repository.create(entity)

        dto = UserDTO(
            id=instance.id,
            email=instance.email,
            username=instance.username,
            access_token=instance.access_token,
            is_active=instance.is_active,
        )

        return {"message": "Created!", "data": dto}

    async def get(self, dto: UserGetDTO) -> dict[str, UserDTO]:
        instance = await self.repository.get(dto.id)

        dto = UserDTO(
            id=instance.id,
            email=instance.email,
            access_token=instance.access_token,
            username=instance.username,
            is_active=instance.is_active,
        )

        return {"message": "Ok!", "data": dto}

    async def login(self, dto: LoginDTO) -> dict[str, TokenDTO]:
        paswd = dto.password.get_secret_value()

        try:
            instance = await self.repository.get_by_email(dto.email)
        except EntityNotFoundException:
            raise AuthErrorException("Invalid password or email!")

        if not instance.is_active:
            raise AuthErrorException("User is not active!")

        if not verify_password(paswd, instance.password):
            raise AuthErrorException("Invalid password or email!")

        if decode_jwt(instance.access_token, current_config.jwt_secret_key) is None:
            instance = await self.repository.set_access_token(instance.id)

        dto = TokenDTO(access_token=instance.access_token, token_type="bearer")

        return {"message": "Authenticated!", "data": dto}

    async def get_by_email(self, dto: UserGetByEmailDTO) -> dict[str, UserDTO]:
        instance = await self.repository.get_by_email(dto.email)

        dto = UserDTO(
            id=instance.id,
            email=instance.email,
            access_token=instance.access_token,
            username=instance.username,
            is_active=instance.is_active,
        )

        return {"message": "Ok!", "data": dto}

    async def get_by_access_token(
        self, dto: UserGetByAccessTokenDTO
    ) -> dict[str, UserDTO]:
        instance = await self.repository.get_by_access_token(dto.access_token)

        dto = UserDTO(
            id=instance.id,
            email=instance.email,
            access_token=instance.access_token,
            username=instance.username,
            is_active=instance.is_active,
        )

        return {"message": "Ok!", "data": dto}
