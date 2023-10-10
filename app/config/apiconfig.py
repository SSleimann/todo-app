from pydantic_settings import BaseSettings

from cachetools import TTLCache

class AppSettings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///db.db"
    jwt_secret_key: str = (
        "eb02980489685d06ac9f99501898a569ed692e4bf673b29b7c48ce00e489c77b"
    )
    access_token_expire_minutes: int = 120
    mem_cache_expire_time_seconds: int = 300


current_config = AppSettings()
mem_cache = TTLCache(maxsize=100, ttl=current_config.mem_cache_expire_time_seconds)