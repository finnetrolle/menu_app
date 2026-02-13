from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = "sqlite:///./menu.db"
    
    # API
    api_prefix: str = "/api"
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost", "http://127.0.0.1:3000"]
    
    # App
    app_name: str = "Menu Management API"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
