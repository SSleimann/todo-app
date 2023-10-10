import pytest

from app.config.security import gen_hashed_password
from app.modules.user.infrastructure.models import UserModel
from app.kernel.domain.value_objects import ValueUUID
from app.modules.user.domain.value_objects import Email

from app.modules.user.infrastructure.repository import UserRepository
from app.modules.user.application.dto import (
    LoginDTO,
    UserCreationDTO,
)
from app.modules.user.application.service import UserService
from app.kernel.domain.exceptions import AuthErrorException

pytestmark = pytest.mark.anyio


async def test_user_create_service(session):
    repo = UserRepository(session)
    service = UserService(repo)

    dto = UserCreationDTO(
        email="test1@email.com",
        password="xxxpass",
        confirm_password="xxxpass",
        username="testusername",
    )

    user = await service.create(dto)
    user_data = user["data"]
    user_message = user["message"]

    assert user_message == "Created!"
    assert user_data.email == dto.email
    assert user_data.username == dto.username


async def test_user_get_service(session, user_test):
    repo = UserRepository(session)
    service = UserService(repo)

    user = await service.get(user_test.id)
    user_data = user["data"]
    user_message = user["message"]

    assert user_message == "Ok!"
    assert user_data.email == user_test.email
    assert user_data.username == user_test.username
    assert user_data.id == user_test.id


async def test_user_get_by_email_service(session, user_test):
    repo = UserRepository(session)
    service = UserService(repo)

    user = await service.get_by_email(Email(user_test.email))
    user_data = user["data"]
    user_message = user["message"]

    assert user_message == "Ok!"
    assert user_data.email == user_test.email
    assert user_data.username == user_test.username


async def test_user_get_by_access_token(session, user_test):
    repo = UserRepository(session)
    service = UserService(repo)

    user = await service.get_by_access_token(user_test.access_token)
    user_data = user["data"]
    user_message = user["message"]

    assert user_message == "Ok!"
    assert user_data.email == user_test.email
    assert user_data.username == user_test.username
    assert user_data.access_token == user_test.access_token


async def test_user_login(session, user_test):
    repo = UserRepository(session)
    service = UserService(repo)
    dto = LoginDTO(email=user_test.email, password="testpass")

    user = await service.login(dto)
    user_data = user["data"]
    user_message = user["message"]

    new_user_token = user_test.access_token

    assert user_message == "Authenticated!"
    assert user_data.access_token == new_user_token


async def test_user_login_invalid_email(session):
    repo = UserRepository(session)
    service = UserService(repo)
    dto = LoginDTO(email="XD@email.com", password="testpass")

    with pytest.raises(AuthErrorException, match="Invalid password or email!"):
        await service.login(dto)


async def test_user_login_invalid_passwd(session, user_test):
    repo = UserRepository(session)
    service = UserService(repo)
    dto = LoginDTO(email=user_test.email, password="XXXXX")

    with pytest.raises(AuthErrorException, match="Invalid password or email!"):
        await service.login(dto)


async def test_user_activate_account(session, user_test):
    repo = UserRepository(session)
    service = UserService(repo)

    user_test.is_active = False
    await session.commit()

    result = await service.activate_account(user_test.id)

    assert result.is_active == True
    assert user_test.is_active == True
    assert result.id == user_test.id
