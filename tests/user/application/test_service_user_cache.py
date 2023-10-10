import pytest

from anyio import sleep
from cachetools import TTLCache

from app.config.apiconfig import current_config
from app.modules.cache.infrastructure.repository import MemoryCacheRepository
from app.modules.user.infrastructure.repository import UserRepository
from app.modules.user.domain.exceptions import CodeActivationExists
from app.modules.user.application.service import UserService, UserCacheService
from app.modules.cache.application.service import CacheService
from app.kernel.domain.exceptions import AuthErrorException

pytestmark = pytest.mark.anyio

async def test_get_code_for_activation(session, user_test):
    mem_cache = TTLCache(maxsize=100, ttl=current_config.mem_cache_expire_time_seconds)
    user_repo, cache_repo = UserRepository(session), MemoryCacheRepository(mem_cache)
    user_service, cache_service = UserService(user_repo), CacheService(cache_repo)
    user_cache_service = UserCacheService(cache_service, user_service)
    
    user_test.is_active = False
    await session.commit()
    
    result = await user_cache_service.get_code_for_activation(user_test.id)
    
    assert result.user_id == user_test.id
    assert result.code is not None
    assert mem_cache.get(user_test.id)
    assert result.expiration_time is not None
    
async def test_get_code_for_activation_user_active(session, user_test):
    mem_cache = TTLCache(maxsize=100, ttl=current_config.mem_cache_expire_time_seconds)
    user_repo, cache_repo = UserRepository(session), MemoryCacheRepository(mem_cache)
    user_service, cache_service = UserService(user_repo), CacheService(cache_repo)
    user_cache_service = UserCacheService(cache_service, user_service)
    
    with pytest.raises(AuthErrorException, match="User is active!"):
        await user_cache_service.get_code_for_activation(user_test.id)
    
async def test_get_code_for_activation_code_activation_exists(session, user_test):
    mem_cache = TTLCache(maxsize=100, ttl=current_config.mem_cache_expire_time_seconds)
    user_repo, cache_repo = UserRepository(session), MemoryCacheRepository(mem_cache)
    user_service, cache_service = UserService(user_repo), CacheService(cache_repo)
    user_cache_service = UserCacheService(cache_service, user_service)
    
    user_test.is_active = False
    await session.commit()
    
    await user_cache_service.get_code_for_activation(user_test.id)
    
    with pytest.raises(CodeActivationExists):
        await user_cache_service.get_code_for_activation(user_test.id)
    
async def test_get_code_for_activation_code_activation_expire(session, user_test):
    mem_cache = TTLCache(maxsize=100, ttl=3)
    user_repo, cache_repo = UserRepository(session), MemoryCacheRepository(mem_cache)
    user_service, cache_service = UserService(user_repo), CacheService(cache_repo)
    user_cache_service = UserCacheService(cache_service, user_service)
    
    user_test.is_active = False
    await session.commit()
    
    firstResult = await user_cache_service.get_code_for_activation(user_test.id)
    await sleep(5)
    cache_exists = mem_cache.get(user_test.id, None)
    
    secondResult = await user_cache_service.get_code_for_activation(user_test.id)
    
    assert secondResult and firstResult
    assert secondResult.code != firstResult.code
    assert firstResult.user_id == secondResult.user_id
    assert cache_exists is None
    
async def test_activate_account_service(session, user_test):
    mem_cache = TTLCache(maxsize=100, ttl=current_config.mem_cache_expire_time_seconds)
    user_repo, cache_repo = UserRepository(session), MemoryCacheRepository(mem_cache)
    user_service, cache_service = UserService(user_repo), CacheService(cache_repo)
    user_cache_service = UserCacheService(cache_service, user_service)
    
    user_test.is_active = False
    await session.commit()
    
    code = await user_cache_service.get_code_for_activation(user_test.id)
    
    result = await user_cache_service.activate_account(code.user_id, code.code)
    
    assert result.is_active == True
    assert user_test.is_active == True
    assert mem_cache.get(user_test.id, None) is None
    assert result.id == user_test.id
    
async def test_activate_account_service_code_not_found(session, user_test):
    mem_cache = TTLCache(maxsize=100, ttl=current_config.mem_cache_expire_time_seconds)
    user_repo, cache_repo = UserRepository(session), MemoryCacheRepository(mem_cache)
    user_service, cache_service = UserService(user_repo), CacheService(cache_repo)
    user_cache_service = UserCacheService(cache_service, user_service)
    
    user_test.is_active = False
    await session.commit()
    
    with pytest.raises(AuthErrorException, match="Code invalid!"):
        await user_cache_service.activate_account(user_test.id, code="aaaa")
    