from pytest import raises

from app.modules.cache.infrastructure.repository import MemoryCacheRepository
from app.modules.cache.domain.entities import CacheDataEntity
from app.kernel.domain.exceptions import EntityNotFoundException

from cachetools import TTLCache

CACHE = TTLCache(maxsize=100, ttl=100)


def test_cache_create_repository():
    repo = MemoryCacheRepository(CACHE)
    entity = CacheDataEntity(id=CacheDataEntity.next_id(), data=bytes("test", "utf-8"))

    newEntity = repo.create(entity)

    assert newEntity.id == entity.id
    assert newEntity.data == entity.data
    assert CACHE[newEntity.id]
    assert CACHE[entity.id].data == newEntity.data


def test_cache_get_repository():
    repo = MemoryCacheRepository(CACHE)
    entity = CacheDataEntity(id=CacheDataEntity.next_id(), data=bytes("test", "utf-8"))

    newEntity = repo.create(entity)

    assert repo.get(entity.id) == newEntity


def test_cache_delete_repository():
    repo = MemoryCacheRepository(CACHE)
    entity = CacheDataEntity(id=CacheDataEntity.next_id(), data=bytes("test", "utf-8"))

    newEntity = repo.create(entity)

    assert repo.delete(entity.id) == newEntity

    with raises(EntityNotFoundException):
        repo.get(entity.id)


def test_cache_update_repository():
    repo = MemoryCacheRepository(CACHE)
    entity = CacheDataEntity(id=CacheDataEntity.next_id(), data=bytes("test", "utf-8"))

    newEntity = repo.create(entity)
    newEntityData = newEntity.data

    payload = {"data": bytes("test2", "utf-8")}

    updatedEntity = repo.update(entity.id, payload)

    assert updatedEntity.data != newEntityData
    assert updatedEntity.data == payload["data"]
    assert CACHE[updatedEntity.id].data == payload["data"]
