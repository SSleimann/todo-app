import abc

from typing import Any, TypeVar

from app.kernel.domain.entities import Entity

MapperModel = TypeVar("MapperModel", bound=Any)
MapperEntity = TypeVar("MapperEntity", bound=Entity)


class BaseMapper(abc.ABC):
    @abc.abstractmethod
    def model_to_entity(self, instance: MapperModel) -> MapperEntity:
        raise NotImplementedError()

    @abc.abstractmethod
    def entity_to_model(self, entity: MapperEntity) -> MapperModel:
        raise NotImplementedError()
