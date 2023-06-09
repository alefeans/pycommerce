from typing import Literal
from functools import lru_cache
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    ENV: Literal["test", "dev", "prod"] = "dev"
    LOG_LEVEL: Literal["critical", "error", "warning", "info", "debug", "trace"] = "info"
    DB_URL: str = ""
    APP_DEBUG: bool = True
    APP_DESCRIPTION: str = "Ecommerce Example Application"
    APP_TITLE: str = "PyCommerce"
    APP_VERSION: str = "0.0.1"
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8080
    SERVER_RELOAD: bool = True
    JWT_SECRET_KEY: str = "unsafe"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("DB_URL")
    def check_db_url(cls, db_url):
        if not db_url:
            raise ValueError("Database URL cannot be empty")
        return db_url


@lru_cache()
def get_settings() -> Settings:
    return Settings()
