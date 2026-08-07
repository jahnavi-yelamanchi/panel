from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="PANEL_")

    environment: str = "local"
    database_url: str = "postgresql+psycopg://panel:panel@localhost:5432/panel"
    asset_bucket: str = "panel-local-assets"
    aws_region: str = "us-east-1"
    s3_endpoint_url: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
