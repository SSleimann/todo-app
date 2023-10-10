from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.config.security import create_access_token
from app.config.apiconfig import current_config
from app.kernel.domain.exceptions import EntityNotFoundException, EntityExists
from app.kernel.domain.value_objects import ValueUUID
from app.kernel.infrastructure.repository import SQLAlchemyRepository
from app.modules.user.domain.repository import UserInterfaceRepository
from app.modules.user.infrastructure.mapper import UserMapper
from app.modules.user.infrastructure.models import UserModel
from app.modules.user.domain.value_objects import Email
from app.modules.user.domain.entities import UserEntity


class UserRepository(UserInterfaceRepository, SQLAlchemyRepository):
    mapper_class = UserMapper
    model_class = UserModel

    async def create(self, entity: UserEntity) -> UserEntity:
        instance = self.entity_to_model(entity)

        try:
            self._session.add(instance)
            await self._session.commit()
        except IntegrityError:
            await self._session.rollback()
            raise EntityExists

        await self._session.refresh(instance, ["tasks"])
        
        return self.model_to_entity(instance)
    
    async def get_by_email(self, email: Email) -> UserEntity:
        model = self.get_model_class()

        q = await self._session.scalars(select(model).where(model.email == email))
        instance = q.first()

        if instance is None:
            raise EntityNotFoundException

        return self.model_to_entity(instance)

    async def get_by_access_token(self, access_token: str) -> UserEntity:
        model = self.get_model_class()

        q = await self._session.scalars(
            select(model).where(model.access_token == access_token)
        )
        instance = q.first()

        if instance is None:
            raise EntityNotFoundException

        return self.model_to_entity(instance)

    async def set_access_token(self, id: ValueUUID) -> UserEntity:
        model = self.get_model_class()

        instance = await self._session.get(model, id)

        if instance is None:
            raise EntityNotFoundException

        exp_time_token = timedelta(minutes=current_config.access_token_expire_minutes)
        access_token = create_access_token(
            {"sub": instance.email},
            current_config.jwt_secret_key,
            expires_delta=exp_time_token,
        )

        instance.access_token = access_token
        await self._session.commit()
        await self._session.refresh(instance, ["tasks"])

        return self.model_to_entity(instance)

    async def activate_account(self, id: ValueUUID):
        model = self.get_model_class()

        instance = await self._session.get(model, id)
        
        if instance is None:
            raise EntityNotFoundException
        
        instance.is_active = True
        await self._session.commit()
        await self._session.refresh(instance, ["tasks"])
        
        return self.model_to_entity(instance)
        