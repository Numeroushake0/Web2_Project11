import os
from pydantic_settings import BaseSettings
from pydantic.networks import PostgresDsn


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 день
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
