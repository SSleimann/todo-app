import pytest

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.config.security import gen_hashed_password
from app.modules.user.infrastructure.models import UserModel
from app.kernel.domain.value_objects import ValueUUID


id_user_general = ValueUUID.next_id()


@pytest.fixture(scope="function")
async def user_test(session: AsyncSession):
    model = UserModel(
            id=id_user_general,
            email="ultratest@email.com",
            username="usertest",
            password=gen_hashed_password("testpass"),
            access_token="abcde",
            is_active=True,
        )

    session.add(model)
    await session.commit()
    await session.refresh(model, ["tasks"])
    
    yield model
    
    await session.delete(model)
    await session.commit()
