from sqlalchemy import select, update
from dataclasses import asdict

from typing import TypeVar, Any

from app.config.database import get_async_session, AsyncSession
from app.kernel.domain.repository import BaseRepository
from app.kernel.domain.entities import Entity
from app.kernel.domain.value_objects import ValueUUID
from app.kernel.infrastructure.mapper import BaseMapper
from app.kernel.domain.exceptions import EntityNotFoundException

MapperModel = TypeVar("MapperModel", bound=Any)

class SQLAlchemyRepository(BaseRepository):
    mapper_class = type[BaseMapper]
    model_class = type[MapperModel]
        
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def create(self, entity: Entity) -> Entity:
        instance = self.entity_to_model(entity)
        
        self._session.add(instance)
        await self._session.commit()
        
        return self.model_to_entity(instance)
    
    async def delete(self, entity_id: ValueUUID) -> Entity:
        model = self.get_model_class()
        
        instance = await self._session.get(model, entity_id)
        
        if instance is None:
            raise EntityNotFoundException
        
        await self._session.delete(instance)
        await self._session.commit()
        return self.model_to_entity(instance)
    
    async def get(self, entity_id: ValueUUID) -> Entity:
        model = self.get_model_class()
        
        instance = await self._session.get(model, entity_id)
        
        if instance is None:
            raise EntityNotFoundException
        
        entity = self.model_to_entity(instance)
        
        return entity
    
    async def get_all(self) -> list[Entity]:
        model = self.get_model_class()
        
        result = await self._session.scalars(select(model))
        
        if not result:
            raise EntityNotFoundException
        
        instances = result.all()
        
        entities = [self.model_to_entity(instance) for instance in instances]
        return entities
    
    async def update(self, entity: Entity) -> Entity:
        model_class = self.get_model_class()
        instance = await self._session.get(model_class, entity.id)
        data_entity = asdict(entity)
        data_entity.pop('id')
        
        if instance is None:
            raise EntityNotFoundException
        
        for key, value in data_entity.items():
            if value is not None:
                setattr(instance, key, value)
        
        await self._session.commit()
        
        return self.model_to_entity(instance)
    
    @property
    def mapper(self):
        return self.mapper_class()
    
    def get_model_class(self):
        assert self.model_class, f"No model class attribute in {self.__class_.__name__}"
        return self.model_class
    
    def entity_to_model(self, entity: Entity):
        assert self.mapper_class, f"No mapper class attribute in {self.__class_.__name__}"
        return self.mapper.entity_to_model(entity)
    
    def model_to_entity(self, instance: MapperModel):
        assert self.mapper_class, f"No mapper class attribute in {self.__class_.__name__}"
        return self.mapper.model_to_entity(instance)