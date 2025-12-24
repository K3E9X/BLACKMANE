"""
Configuration Settings for BLACKMANE Backend
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    # Application
    app_name: str = "BLACKMANE"
    debug: bool = True

    # Database
    database_url: str = "sqlite:///./blackmane.db"

    # Security
    secret_key: str = "dev-secret-key-change-in-production"  # TODO: Generate secure key
    allowed_hosts: list[str] = ["localhost", "127.0.0.1"]

    # Analysis limits
    max_components: int = 500
    max_flows: int = 1000
    max_zones: int = 50
    analysis_timeout: int = 30  # seconds

    # File uploads (for future image/PDF import)
    max_upload_size: int = 10 * 1024 * 1024  # 10 MB
    upload_dir: str = "./uploads"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
