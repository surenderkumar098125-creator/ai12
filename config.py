from typing import Optional, List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str = Field(...)
    GROQ_API_KEY: Optional[str] = Field(default=None)
    GROQ_MODEL: Optional[str] = Field(default="llama-3.1-8b-instant")

    DATABASE_URL: str = Field(...)
    ADMIN_IDS: List[int] = Field(default_factory=list)

    BACKUP_DIR: str = Field(default="backups/")
    LOG_LEVEL: str = Field(default="INFO")

    # AI specific
    AI_DAILY_LIMIT_FREE: int = Field(default=100)
    AI_DAILY_LIMIT_VIP: int = Field(default=1000)
    AI_DAILY_LIMIT_ADMIN: int = Field(default=0)
    AI_REQUEST_TIMEOUT: int = Field(default=10)
    AI_RETRY_COUNT: int = Field(default=2)

    AI_FALLBACK_RESPONSE: str = Field(
        default="Sorry, I'm having trouble answering right now. Please try again later."
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("ADMIN_IDS", mode="before")
    @classmethod
    def parse_admins(cls, value):
        if value is None or value == "":
            return []

        if isinstance(value, str):
            return [
                int(x.strip())
                for x in value.split(",")
                if x.strip()
            ]

        if isinstance(value, list):
            return [int(x) for x in value]

        return value


settings = Settings()
