from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///db.db"

class TestSettings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///test.db"

current_config = AppSettings()