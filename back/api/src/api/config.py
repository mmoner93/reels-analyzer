from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    # API Settings
    api_title: str = "Instagram Reel Processor"
    api_version: str = "1.0.0"
    api_prefix: str = "/api"
    
    # Database
    database_url: str = "sqlite:///./reels.db"
    
    # Celery/Redis
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    
    # Processing
    temp_dir: str = "./temp"
    
    # CORS
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]


settings = Settings()
