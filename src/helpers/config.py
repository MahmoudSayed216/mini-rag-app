from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    
    APP_NAME: str
    VERSION: str
    OPENAI_API_KEY: str
    MAX_FILE_SIZE: int
    ALLOWED_FILE_TYPES: list

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()