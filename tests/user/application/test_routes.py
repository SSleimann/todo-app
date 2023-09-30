import pytest

from fastapi.testclient import TestClient

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.user.infrastructure.models import UserModel
from app.modules.user.infrastructure.repository import UserRepository
from app.kernel.domain.value_objects import ValueUUID
from app.config.security import gen_hashed_password, decode_jwt
from app.config.apiconfig import current_config

pytestmark = pytest.mark.anyio


async def test_register_route(api_client: TestClient, session: AsyncSession):
    payload = {
        "email": "emailtest@email.com",
        "password": "test_passw",
        "confirm_password": "test_passw",
        "username": "testusername",
    }

    res = api_client.post("/user/register", json=payload)
    data = res.json()

    u = await session.get(UserModel, data["data"]["id"])

    assert data["message"] == "Created!"
    assert res.status_code == 201
    assert data["data"]["email"] == payload["email"]
    assert data["data"]["username"] == payload["username"]
    assert data["data"]["is_active"] == True
    assert data["data"]["access_token"] == None
    assert u is not None


async def test_login_route(api_client: TestClient, session: AsyncSession):
    user = UserModel(
        id=ValueUUID.next_id(),
        username="euser",
        password=gen_hashed_password("testpass"),
        email="emaile@email.com",
        access_token=None,
        is_active=True,
    )

    session.add(user)
    await session.commit()

    payload = {"email": "emaile@email.com", "password": "testpass"}

    res = api_client.post("/user/login", json=payload)
    data = res.json()

    assert data["message"] == "Authenticated!"
    assert res.status_code == 200
    assert data["data"]["access_token"] is not None
    assert data["data"]["token_type"] == "bearer"
    assert user.access_token is not None
    assert (
        decode_jwt(user.access_token, current_config.jwt_secret_key)["sub"]
        == payload["email"]
    )


async def test_get_user_me(api_client: TestClient, session: AsyncSession):
    user = UserModel(
        id=ValueUUID.next_id(),
        username="euser",
        password=gen_hashed_password("testpass"),
        email="emasile@email.com",
        access_token=None,
        is_active=True,
    )

    session.add(user)
    await session.commit()

    repo = UserRepository(session)
    await repo.set_access_token(user.id)

    res = api_client.get(
        "/user/me", headers={"Authorization": f"Bearer {user.access_token}"}
    )
    data = res.json()

    assert data["message"] == "Ok!"
    assert data["data"]["email"] == user.email
    assert data["data"]["username"] == user.username
    assert data["data"]["is_active"] == user.is_active
