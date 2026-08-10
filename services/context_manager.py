from __future__ import annotations
from typing import List, Optional, Tuple
from database.database import AsyncSessionLocal
from database.models import Conversation, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
import asyncio
import math

# Simple character-based trimming to approximately control tokens
MAX_CONTEXT_CHARS = 4000

async def get_or_create_conversation(conversation_id: str, user_id: int, session: Optional[AsyncSession] = None) -> Conversation:
    close = False
    if session is None:
        session = AsyncSessionLocal()
        close = True
    async with session as s:
        q = await s.execute(select(Conversation).where(Conversation.conversation_id == conversation_id, Conversation.user_id == user_id))
        conv = q.scalars().first()
        if conv:
            return conv
        conv = Conversation(conversation_id=conversation_id, user_id=user_id, metadata={})
        s.add(conv)
        await s.commit()
        await s.refresh(conv)
        return conv

async def append_message(conversation: Conversation, role: str, content: str, session: Optional[AsyncSession] = None) -> Message:
    close = False
    if session is None:
        session = AsyncSessionLocal()
        close = True
    async with session as s:
        msg = Message(conversation_id=conversation.id, role=role, content=content, created_at=datetime.utcnow())
        s.add(msg)
        await s.commit()
        await s.refresh(msg)
        return msg

async def get_conversation_messages(conversation: Conversation, limit: int = 50, session: Optional[AsyncSession] = None) -> List[Message]:
    close = False
    if session is None:
        session = AsyncSessionLocal()
        close = True
    async with session as s:
        q = await s.execute(select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at.asc()).limit(limit))
        return q.scalars().all()

async def clear_conversation(conversation: Conversation, session: Optional[AsyncSession] = None):
    if session is None:
        session = AsyncSessionLocal()
    async with session as s:
        await s.execute("DELETE FROM messages WHERE conversation_id = :cid", {"cid": conversation.id})
        await s.commit()

async def trim_context(conversation: Conversation, max_chars: int = MAX_CONTEXT_CHARS, session: Optional[AsyncSession] = None):
    """Trim oldest messages until total chars under limit."""
    if session is None:
        session = AsyncSessionLocal()
    async with session as s:
        q = await s.execute(select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at.asc()))
        msgs = q.scalars().all()
        total = sum(len(m.content or "") for m in msgs)
        if total <= max_chars:
            return
        # drop oldest until under limit
        idx = 0
        while total > max_chars and idx < len(msgs):
            total -= len(msgs[idx].content or "")
            await s.delete(msgs[idx])
            idx += 1
        await s.commit()
