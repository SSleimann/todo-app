from app.kernel.domain.exceptions import EntityNotFoundException
from app.kernel.domain.value_objects import ValueUUID
from app.modules.cache.domain.entities import CacheDataEntity
from app.modules.cache.domain.repository import MemoryCacheRepositoryInterface
from app.kernel.domain.repository import BaseRepository

from cachetools import TTLCache

from typing import Any


class CacheRepository(BaseRepository):
    def __init__(self, cache: Any):
        self.cache = cache

class MemoryCacheRepository(MemoryCacheRepositoryInterface, CacheRepository):
    def __init__(self, cache: TTLCache):
        super().__init__(cache)
    
    def create(self, entity: CacheDataEntity) -> CacheDataEntity:
        self.cache[entity.id] = entity
        return self.cache[entity.id]
    
    def get(self, id: ValueUUID) -> CacheDataEntity:
        try:
            entity = self.cache[id]
        except KeyError:
            raise EntityNotFoundException
        
        return entity
    
    def delete(self, id: ValueUUID) -> CacheDataEntity:
        try:
            entity = self.cache[id]
            del self.cache[id]
        except KeyError:
            raise EntityNotFoundException
        
        return entity
    
    def update(self, id: ValueUUID, params: dict[Any, bytes]) -> CacheDataEntity:
        
        try:
            entity = self.cache[id]
        except KeyError:
            raise EntityNotFoundException
        
        for k, v in params.items():
            current_value = getattr(entity, k, None)
            if current_value is not None:
                setattr(entity, k, v)
                
        self.cache[id] = entity
        
        return entity