from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = "postgresql://postgres:postgres@db:5432/menu_db"
    
    # PostgreSQL connection parameters (for individual configuration)
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "menu_db"
    db_host: str = "db"
    db_port: int = 5432
    
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
