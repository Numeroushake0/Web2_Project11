from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.networks import PostgresDsn

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    SECRET_KEY: str = "supersecretkey"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    algorithm: str = "HS256"
    frontend_url: str = "http://localhost:8000"
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = "your_email@gmail.com"
    smtp_password: str = "your_email_password"
    cloudinary_name: str = "your_cloud_name"
    cloudinary_api_key: str = "your_api_key"
    cloudinary_api_secret: str = "your_api_secret"
    redis_host: str = "redis"
    redis_port: int = 6379

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"  
    )

settings = Settings()
