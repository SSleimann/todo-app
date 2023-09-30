import pytest
import anyio

from jose import jwt

from app.config.apiconfig import current_config
from app.modules.user.infrastructure.repository import UserRepository
from app.modules.user.domain.value_objects import Email
from app.modules.user.domain.entities import UserEntity
from app.kernel.domain.exceptions import EntityNotFoundException

pytestmark = pytest.mark.anyio


async def test_repository_get_by_email(session, user_test):
    repo = UserRepository(session)
    email = Email(user_test.email)
    result = await repo.get_by_email(email)

    assert result.email == email
    assert result.email == user_test.email
    assert isinstance(result, UserEntity)


async def test_repository_get_by_access_token(session, user_test):
    repo = UserRepository(session)
    
    result = await repo.get_by_access_token(user_test.access_token)

    assert result.access_token == user_test.access_token
    assert isinstance(result, UserEntity)


async def test_exceptions_repo(session):
    repo = UserRepository(session)

    with pytest.raises(EntityNotFoundException):
        await repo.get_by_email(Email("eeeeeeeeeeeeeeee@email.com"))

    with pytest.raises(EntityNotFoundException):
        await repo.get_by_access_token("xxxx")

async def test_repository_set_access_token(session, user_test):
    repo = UserRepository(session)
    
    instance = await repo.set_access_token(user_test.id)
    token_user = jwt.decode(instance.access_token, current_config.jwt_secret_key)
    
    assert instance.access_token is not None
    assert instance.access_token == user_test.access_token
    assert token_user["sub"] == instance.email