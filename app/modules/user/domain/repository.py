from abc import ABC, abstractmethod

from app.kernel.domain.repository import BaseRepository
from app.modules.user.domain.entities import UserEntity
from app.modules.user.domain.value_objects import Email
from app.kernel.domain.value_objects import ValueUUID


class UserInterfaceRepository(BaseRepository, ABC):
    """Interface for User repository"""

    @abstractmethod
    async def get_by_email(self, email: Email) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_access_token(self, access_token: str) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    async def set_access_token(self, id: ValueUUID) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    async def activate_account(self, id: ValueUUID) -> UserEntity:
        raise NotImplementedError
