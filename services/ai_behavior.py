from __future__ import annotations
from typing import Optional
from services.ai_service import get_ai_service
from services.context_manager import get_or_create_conversation, append_message, trim_context, get_conversation_messages
from utils.language import detect_language, Language
from database.models import AIRequest
from database.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings
import asyncio
import logging

logger = logging.getLogger("preeti.ai_behavior")

async def prepare_prompt(user_id: int, conversation_id: str, user_text: str, max_chars: int = 3000) -> str:
    conv = await get_or_create_conversation(conversation_id, user_id)
    await append_message(conv, "user", user_text)
    await trim_context(conv, max_chars)
    msgs = await get_conversation_messages(conv, limit=50)
    # Build a simple prompt with system instructions + conversation
    lang = detect_language(user_text)
    system = (
        "You are Preeti, a friendly, smart, playful and helpful assistant. Respond naturally in the user's language "
        "(Hindi, Hinglish, or English) and adapt tone based on the user's message. Be concise when appropriate."
    )
    pieces = [f"System: {system}"]
    for m in msgs:
        role = m.role.capitalize()
        pieces.append(f"{role}: {m.content}")
    pieces.append(f"User: {user_text}")
    prompt = "\n".join(pieces)
    return prompt

async def ask_ai(user_id: int, conversation_id: str, text: str) -> str:
    ai = get_ai_service()
    prompt = await prepare_prompt(user_id, conversation_id, text)
    # Save ai request entry
    async with AsyncSessionLocal() as s:
        req = AIRequest(user_id=user_id, conversation_id=conversation_id, prompt_hash="", model=ai.model)
        s.add(req)
        await s.commit()
        await s.refresh(req)
        req_id = req.id
    try:
        resp = await ai.generate(prompt)
        # append assistant reply
        async with AsyncSessionLocal() as s:
            conv = await get_or_create_conversation(conversation_id, user_id, session=s)
            await append_message(conv, "assistant", resp, session=s)
            # mark request success
            r = await s.get(AIRequest, req_id)
            r.status = "success"
            await s.commit()
        return resp
    except Exception as e:
        logger.exception("AI request failed")
        # mark failed
        async with AsyncSessionLocal() as s:
            r = await s.get(AIRequest, req_id)
            r.status = "error"
            r.metadata = {"error": str(e)}
            await s.commit()
        return settings.AI_FALLBACK_RESPONSE
