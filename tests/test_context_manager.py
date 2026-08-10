# tests/test_context_manager.py
import pytest
import asyncio
from services.context_manager import get_or_create_conversation, append_message, get_conversation_messages, clear_conversation
from database.models import Conversation

@pytest.mark.asyncio
async def test_conversation_lifecycle():
    conv = await get_or_create_conversation("testconv", 12345)
    assert isinstance(conv, Conversation)
    msg = await append_message(conv, "user", "hello")
    msgs = await get_conversation_messages(conv)
    assert any(m.content == "hello" for m in msgs)
    await clear_conversation(conv)
    msgs = await get_conversation_messages(conv)
    assert len(msgs) == 0
