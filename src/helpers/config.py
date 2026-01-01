from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    
    APP_NAME: str
    VERSION: str
    OPENAI_API_KEY: str
    MAX_FILE_SIZE: int
    ALLOWED_FILE_TYPES: list
    FILE_DEFAULT_CHUNK_SIZE: int
    #mongodb
    MONGODB_URL: str
    MONGODB_DATABASE: str
    class Config:
        env_file = "/home/mahmoud-sayed/Desktop/Code/Python/mini-rag/mini-rag/src/.env"


@lru_cache
def get_settings():
    return Settings()