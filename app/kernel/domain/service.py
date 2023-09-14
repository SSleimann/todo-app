import abc

from app.kernel.domain.repository import BaseRepository

class BaseService(abc.ABC):
    def __init__(self, repository: BaseRepository) -> None:
        self.repository = repository
    