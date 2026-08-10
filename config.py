from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings using pydantic v2 / pydantic-settings.

    Uses SettingsConfigDict to load .env and keep backward-compatible field names.
    """
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    BOT_TOKEN: str = Field(..., env="BOT_TOKEN")
    GROQ_API_KEY: Optional[str] = Field(None, env="GROQ_API_KEY")
    GROQ_MODEL: str = Field("gpt-1", env="GROQ_MODEL")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    ADMIN_IDS: List[int] = Field(default_factory=list, env="ADMIN_IDS")
    BACKUP_DIR: str = Field("backups/", env="BACKUP_DIR")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")

    # AI specific
    AI_DAILY_LIMIT_FREE: int = Field(100, env="AI_DAILY_LIMIT_FREE")
    AI_DAILY_LIMIT_VIP: int = Field(1000, env="AI_DAILY_LIMIT_VIP")
    AI_DAILY_LIMIT_ADMIN: int = Field(0, env="AI_DAILY_LIMIT_ADMIN")
    AI_REQUEST_TIMEOUT: int = Field(10, env="AI_REQUEST_TIMEOUT")
    AI_RETRY_COUNT: int = Field(2, env="AI_RETRY_COUNT")
    AI_FALLBACK_RESPONSE: str = Field(
        "Sorry, I'm having trouble answering right now. Please try again later.", env="AI_FALLBACK_RESPONSE"
    )

    @field_validator("ADMIN_IDS", mode="before")
    def _parse_admins(cls, v):
        # Accept comma-separated string or list of ints
        if isinstance(v, str):
            parts = [p.strip() for p in v.split(",") if p.strip()]
            try:
                return [int(x) for x in parts]
            except Exception:
                # if parsing fails, return empty list to avoid hard crash here;
                # field-level validation will raise if required elsewhere
                return []
        return v


settings = Settings()
