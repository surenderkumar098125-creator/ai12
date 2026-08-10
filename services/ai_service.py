from __future__ import annotations
import asyncio
from typing import Optional, Any
import httpx
import backoff
from config import settings
import logging

logger = logging.getLogger("preeti.ai_service")

GROQ_API_BASE = "https://api.groq.com/v1"

class GroqAPIError(Exception):
    pass

class AIService:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.GROQ_API_KEY
        self.model = model or settings.GROQ_MODEL
        self.timeout = settings.AI_REQUEST_TIMEOUT
        self.retries = settings.AI_RETRY_COUNT

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def _post(self, payload: dict) -> dict:
        url = f"{GROQ_API_BASE}/models/{self.model}/completions"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, json=payload, headers=self._headers())
            if response.status_code != 200:
                raise GroqAPIError(f"Groq API error {response.status_code}: {response.text}")
            return response.json()

    async def generate(self, prompt: str, max_tokens: int = 1024, stop: Optional[list] = None) -> str:
        if not self.api_key:
            raise GroqAPIError("No GROQ API key configured")

        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens,
        }
        if stop:
            payload["stop"] = stop

        # Exponential backoff for transient errors
        for attempt in range(self.retries + 1):
            try:
                data = await self._post(payload)
                # adapt to Groq response format; expect data["choices"][0]["text"] or similar
                if isinstance(data, dict) and "choices" in data and data["choices"]:
                    text = data["choices"][0].get("text") or data["choices"][0].get("message")
                    return text or ""
                # fallback: return a stringified result
                return str(data)
            except Exception as e:
                logger.debug("Groq attempt %s failed: %s", attempt + 1, str(e))
                # last attempt -> raise
                if attempt == self.retries:
                    raise
                await asyncio.sleep(1 + attempt * 1.5)

# Singleton helper
_ai_service = None

def get_ai_service() -> AIService:
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
