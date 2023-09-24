import pytest

from app.modules.user.infrastructure.repository import UserRepository
from app.modules.user.domain.value_objects import Email
from app.modules.user.infrastructure.models import UserModel
from app.modules.user.domain.entities import UserEntity
from app.kernel.domain.exceptions import EntityNotFoundException

pytestmark = pytest.mark.anyio


async def test_repository_get_by_email(session):
    user_model = UserModel(
        id=UserEntity.next_id(),
        email=Email("email@gmail.com"),
        password="testpass",
        access_token="akakskaskak",
        is_active=True,
        username="test_user",
    )

    session.add(user_model)
    await session.commit()

    repo = UserRepository(session)
    email = Email("email@gmail.com")
    result = await repo.get_by_email(email)

    assert result.email == email
    assert isinstance(result, UserEntity)


async def test_repository_get_by_access_token(session):
    user_model = UserModel(
        id=UserEntity.next_id(),
        email=Email("email2@gmail.com"),
        password="testpass",
        access_token="eeeee",
        is_active=True,
        username="test_user",
    )

    session.add(user_model)
    await session.commit()

    repo = UserRepository(session)
    token = "eeeee"
    result = await repo.get_by_access_token(token)

    assert result.access_token == token
    assert isinstance(result, UserEntity)


async def test_exceptions_repo(session):
    repo = UserRepository(session)

    with pytest.raises(EntityNotFoundException):
        await repo.get_by_email(Email("eeeeeeeeeeeeeeee@email.com"))

    with pytest.raises(EntityNotFoundException):
        await repo.get_by_access_token("xxxx")
