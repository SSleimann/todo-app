from app.kernel.domain.service import BaseService
from app.kernel.domain.value_objects import ValueUUID
from app.modules.cache.domain.entities import CacheDataEntity
from app.modules.cache.application.dto import (
    AddToCacheDTO,
    UpdateToCacheDTO,
    CacheDataDTO,
)


class CacheService(BaseService):
    def get(self, id: ValueUUID) -> CacheDataDTO:
        result = self.repository.get(id)
        return CacheDataDTO(id=result.id, data=result.data)

    def create(self, dto: AddToCacheDTO) -> CacheDataDTO:
        entity = CacheDataEntity(id=dto.id, data=dto.data)

        result = self.repository.create(entity)

        return CacheDataDTO(id=result.id, data=result.data)

    def update(self, id: ValueUUID, dto: UpdateToCacheDTO) -> CacheDataDTO:
        result = self.repository.update(id, dto.model_dump())
        return CacheDataDTO(id=result.id, data=result.data)

    def delete(self, id: ValueUUID) -> CacheDataDTO:
        result = self.repository.delete(id)
        return CacheDataDTO(id=result.id, data=result.data)
