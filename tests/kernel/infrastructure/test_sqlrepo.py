import uuid
import dataclasses
import pytest

from sqlalchemy import Column, String, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import Base, GUID
from app.kernel.domain.entities import Entity
from app.kernel.domain.exceptions import EntityNotFoundException
from app.kernel.domain.value_objects import ValueUUID
from app.kernel.infrastructure.repository import SQLAlchemyRepository
from app.kernel.infrastructure.mapper import BaseMapper

pytestmark = pytest.mark.anyio


@dataclasses.dataclass
class UserEntity(Entity):
    name: str
    description: str = None


class UserModel(Base):
    __tablename__ = "user_tests"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(String, nullable=True)


class UserMapper(BaseMapper):
    def model_to_entity(self, instance: UserModel) -> UserEntity:
        return UserEntity(
            id=instance.id, name=instance.name, description=instance.description
        )

    def entity_to_model(self, entity: UserEntity) -> UserModel:
        return UserModel(id=entity.id, name=entity.name, description=entity.description)


class UserRepository(SQLAlchemyRepository):
    mapper_class = UserMapper
    model_class = UserModel


async def test_sqlalchemy_repository_create(session: AsyncSession):
    user1 = UserEntity(id=ValueUUID.next_id(), name="juan pablo")
    repository = UserRepository(session)

    newEntity = await repository.create(user1)
    result = await session.scalars(select(UserModel))

    instances = result.all()

    assert instances[0].id == newEntity.id
    assert len(instances) == 1


async def test_sqlalchemy_repository_delete(session: AsyncSession):
    user1 = UserEntity(id=ValueUUID.next_id(), name="juanp ablo")
    repo = UserRepository(session)

    await repo.create(user1)

    await repo.delete(user1.id)
    result = await session.scalar(select(UserModel).where(UserModel.id == user1.id))

    assert result is None


async def test_sqlalchemy_repository_get(session: AsyncSession):
    user1 = UserEntity(id=ValueUUID.next_id(), name="juanp ablo")
    repo = UserRepository(session)

    result = await repo.create(user1)

    assert result.id == user1.id
    assert result.name == user1.name


async def test_sqlalchemy_repository_update(session: AsyncSession):
    user1 = UserEntity(id=ValueUUID.next_id(), name="juanp ablo1")
    repo = UserRepository(session)
    newEntity: UserEntity = await repo.create(user1)
    newEntity.name = "hola"

    result = await repo.update(newEntity.id, {"name": newEntity.name})

    assert result.id == newEntity.id
    assert result.name == "hola"


async def test_sqlalchemy_repository_get_all_paginated(session: AsyncSession):
    repo = UserRepository(session)

    instances = await repo.get_all_paginated()

    assert len(instances) > 0 and len(instances) <= 10


async def test_sqlalchemy_repository_get_by_params(session: AsyncSession):
    repo = UserRepository(session)
    user1 = UserEntity(id=ValueUUID.next_id(), name="jean_carlos")
    newEntity = await repo.create(user1)

    instance = await repo.get_by_params(
        params={"name": newEntity.name, "description": None, "id": newEntity.id}
    )

    assert instance.name == newEntity.name
    assert instance.description is None


async def test_sqlalchemy_repository_errors(session: AsyncSession):
    user = UserEntity(id=ValueUUID.next_id(), name="juanp ablo1")
    repo = UserRepository(session)

    with pytest.raises(EntityNotFoundException):
        await repo.get(user.id)

    with pytest.raises(EntityNotFoundException):
        await repo.delete(user.id)

    with pytest.raises(EntityNotFoundException):
        await repo.update(user.id, params={"name": "XD"})
