import abc

from app.kernel.domain.entities import Entity
from app.kernel.domain.value_objects import ValueUUID


class BaseRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, entity: Entity) -> Entity:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, entity_id: ValueUUID):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, entity_id: ValueUUID) -> Entity:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, entity_id: ValueUUID, params: dict) -> Entity:
        raise NotImplementedError
