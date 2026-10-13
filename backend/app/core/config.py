from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="ATTENDWISE_", extra="ignore")
    database_url: str = "sqlite:///./attendwise.db"
    jwt_secret: str = "development-only-change-me"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60 * 24 * 7
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:4173,http://127.0.0.1:4173"

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
