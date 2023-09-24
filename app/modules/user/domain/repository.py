from abc import ABC

from app.kernel.domain.repository import BaseRepository


class UserInterfaceRepository(BaseRepository, ABC):
    """Interface for User repository"""