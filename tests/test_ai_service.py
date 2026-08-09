# tests/test_ai_service.py
import pytest
import asyncio
from services.ai_service import AIService, GroqAPIError
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_generate_success(monkeypatch):
    svc = AIService(api_key="test", model="gpt-1")
    async def fake_post(self, payload):
        return {"choices": [{"text": "Hello"}]}
    monkeypatch.setattr(svc, "_post", fake_post)
    res = await svc.generate("hi")
    assert "Hello" in res

@pytest.mark.asyncio
async def test_no_api_key():
    svc = AIService(api_key=None, model="gpt-1")
    with pytest.raises(GroqAPIError):
        await svc.generate("hi")
