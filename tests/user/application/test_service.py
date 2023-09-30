import pytest

from app.config.security import gen_hashed_password
from app.modules.user.infrastructure.models import UserModel
from app.kernel.domain.value_objects import ValueUUID

from app.modules.user.infrastructure.repository import UserRepository
from app.modules.user.application.dto import (
    LoginDTO,
    UserCreationDTO,
    UserGetByEmailDTO,
    UserGetDTO,
    UserGetByAccessTokenDTO,
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

    dto = UserGetDTO(id=user_test.id)

    user = await service.get(dto)
    user_data = user["data"]
    user_message = user["message"]

    assert user_message == "Ok!"
    assert user_data.email == user_test.email
    assert user_data.username == user_test.username
    assert user_data.id == user_test.id


async def test_user_get_by_email_service(session, user_test):
    repo = UserRepository(session)
    service = UserService(repo)

    dto = UserGetByEmailDTO(email=user_test.email)

    user = await service.get_by_email(dto)
    user_data = user["data"]
    user_message = user["message"]

    assert user_message == "Ok!"
    assert user_data.email == user_test.email
    assert user_data.username == user_test.username


async def test_user_get_by_access_token(session, user_test):
    repo = UserRepository(session)
    service = UserService(repo)

    dto = UserGetByAccessTokenDTO(access_token=user_test.access_token)

    user = await service.get_by_access_token(dto)
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


async def test_user_login_active_user(session):
    model = UserModel(
        id=ValueUUID.next_id(),
        email="ultrates11t@email.com",
        username="usertest",
        password=gen_hashed_password("testpass"),
        access_token="abcde",
        is_active=False,
    )

    session.add(model)
    await session.commit()

    repo = UserRepository(session)
    service = UserService(repo)
    dto = LoginDTO(email=model.email, password="testpass")

    with pytest.raises(AuthErrorException, match="User is not active!"):
        await service.login(dto)


async def test_user_login_invalid_passwd(session, user_test):
    repo = UserRepository(session)
    service = UserService(repo)
    dto = LoginDTO(email=user_test.email, password="XXXXX")

    with pytest.raises(AuthErrorException, match="Invalid password or email!"):
        await service.login(dto)
