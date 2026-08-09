import asyncio
from typing import List, Optional
from pydantic import BaseSettings, Field, validator

class Settings(BaseSettings):
    BOT_TOKEN: str = Field(..., env="BOT_TOKEN")
    GROQ_API_KEY: Optional[str] = Field(None, env="GROQ_API_KEY")
    GROQ_MODEL: Optional[str] = Field("gpt-1", env="GROQ_MODEL")
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
    AI_FALLBACK_RESPONSE: str = Field("Sorry, I'm having trouble answering right now. Please try again later.", env="AI_FALLBACK_RESPONSE")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("ADMIN_IDS", pre=True)
    def parse_admins(cls, v):
        if isinstance(v, str):
            v = [p for p in (x.strip() for x in v.split(",")) if p]
            return [int(x) for x in v]
        return v

settings = Settings()
