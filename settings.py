import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_name: str = os.getenv("DATABASE_NAME", "tasks.db")
    host: str = os.getenv("APP_HOST", "0.0.0.0")
    port: int = int(os.getenv("APP_PORT", "8000"))
    cors_origins: list[str] = [
        origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",") if origin.strip()
    ] or ["*"]


settings = Settings()
