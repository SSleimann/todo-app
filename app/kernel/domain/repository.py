import abc

from app.kernel.domain.entities import Entity
from app.kernel.domain.value_objects import ValueUUID


class BaseRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, entity: Entity) -> Entity:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, entity_id: ValueUUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, entity_id: ValueUUID) -> Entity:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all(self) -> list[Entity]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, entity: Entity) -> Entity:
        raise NotImplementedError
