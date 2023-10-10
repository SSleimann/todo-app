from pytest import raises

from app.modules.cache.infrastructure.repository import MemoryCacheRepository
from app.modules.cache.application.dto import (
    AddToCacheDTO,
    CacheDataDTO,
    UpdateToCacheDTO,
)
from app.modules.cache.application.service import CacheService
from app.modules.cache.domain.entities import CacheDataEntity
from app.kernel.domain.exceptions import EntityNotFoundException

from cachetools import TTLCache

CACHE = TTLCache(maxsize=100, ttl=100)

firstEntity = CacheDataEntity(
    id=CacheDataEntity.next_id(), data=bytes("testing", "utf-8")
)
CACHE[firstEntity.id] = firstEntity


def test_create_service_cache():
    repo = MemoryCacheRepository(CACHE)
    service = CacheService(repo)
    instance_id = CacheDataEntity.next_id()

    dto = AddToCacheDTO(id=instance_id, data=bytes("test", "utf-8"))
    result = service.create(dto)

    assert result.id == CACHE[result.id].id
    assert instance_id == result.id
    assert result.data == dto.data
    assert isinstance(result, CacheDataDTO)


def test_get_service_cache():
    repo = MemoryCacheRepository(CACHE)
    service = CacheService(repo)

    result = service.get(firstEntity.id)

    assert result.id == CACHE[result.id].id
    assert isinstance(result, CacheDataDTO)


def test_delete_service_cache():
    repo = MemoryCacheRepository(CACHE)
    service = CacheService(repo)

    entity = CacheDataEntity(
        id=CacheDataEntity.next_id(), data=bytes("testing", "utf-8")
    )
    repo.create(entity)

    result = service.delete(entity.id)

    assert result.id == entity.id
    assert isinstance(result, CacheDataDTO)

    with raises(EntityNotFoundException):
        service.get(result.id)
