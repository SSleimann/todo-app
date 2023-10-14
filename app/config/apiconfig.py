from pydantic_settings import BaseSettings

from cachetools import TTLCache


class GlobalSettings(BaseSettings):
    jwt_secret_key: str = (
        "eb02980489685d06ac9f99501898a569ed692e4bf673b29b7c48ce00e489c77b"
    )
    database_url: str = "sqlite+aiosqlite:///db.db"
    access_token_expire_minutes: int = 120
    mem_cache_expire_time_seconds: int = 300


current_config = GlobalSettings()
mem_cache = TTLCache(maxsize=100000, ttl=current_config.mem_cache_expire_time_seconds)
