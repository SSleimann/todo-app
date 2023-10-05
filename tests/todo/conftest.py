import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.security import gen_hashed_password, create_access_token
from app.modules.user.infrastructure.models import UserModel
from app.modules.todo.infrastructure.models import TaskModel
from app.modules.user.domain.value_objects import Email
from app.kernel.domain.value_objects import ValueUUID
from app.config.apiconfig import current_config

paswd_hashed = gen_hashed_password("testpass")
access_token = create_access_token(
    {"sub": "testeremailabsolute@gmail.com"}, current_config.jwt_secret_key
)


@pytest.fixture()
async def user_test(session: AsyncSession):
    user = UserModel(
        id=ValueUUID.next_id(),
        email=Email("testeremailabsolute@gmail.com"),
        username="tester",
        password=paswd_hashed,
        access_token=access_token,
    )

    session.add(user)
    await session.commit()

    yield user

    await session.delete(user)
    await session.commit()


@pytest.fixture()
async def task_test(session: AsyncSession, user_test):
    task = TaskModel(
        id=ValueUUID.next_id(),
        title="test task",
        description="test task description",
        user_id=user_test.id,
    )

    session.add(task)
    await session.commit()

    yield task

    await session.delete(task)
    await session.commit()
