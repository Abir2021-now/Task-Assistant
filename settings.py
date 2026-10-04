import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL") or ""
    database_name: str = os.getenv("DATABASE_NAME", "tasks.db")
    host: str = os.getenv("APP_HOST", "0.0.0.0")
    port: int = int(os.getenv("APP_PORT", "8000"))
    cors_origins: list[str] = field(
        default_factory=lambda: [
            origin.strip()
            for origin in os.getenv("CORS_ORIGINS", "*").split(",")
            if origin.strip()
        ] or ["*"]
    )
    api_token: str | None = os.getenv("API_TOKEN") or None
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
