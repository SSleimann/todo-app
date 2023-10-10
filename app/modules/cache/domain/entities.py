from app.kernel.domain.entities import Entity

from dataclasses import dataclass

@dataclass
class CacheDataEntity(Entity):
    data: bytes
    
