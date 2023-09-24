from sqlalchemy import select

from app.kernel.domain.exceptions import EntityNotFoundException
from app.kernel.infrastructure.repository import SQLAlchemyRepository
from app.modules.user.domain.repository import UserInterfaceRepository
from app.modules.user.infrastructure.mapper import UserMapper
from app.modules.user.infrastructure.models import UserModel
from app.modules.user.domain.value_objects import Email
from app.modules.user.domain.entities import UserEntity


class UserRepository(SQLAlchemyRepository, UserInterfaceRepository):
    mapper_class = UserMapper
    model_class = UserModel

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
