from __future__ import annotations
from typing import Optional, Any, Dict
from database.database import AsyncSessionLocal
from database.content_models import MessageTemplate, MessageVersion, BotSetting
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import datetime

async def get_template(key: str) -> MessageTemplate | None:
    async with AsyncSessionLocal() as s:
        q = await s.execute(select(MessageTemplate).where(MessageTemplate.key == key))
        return q.scalars().first()

async def save_template(key: str, content: str, updated_by: int) -> MessageTemplate:
    async with AsyncSessionLocal() as s:
        tpl = await get_template(key)
        if not tpl:
            tpl = MessageTemplate(key=key, content=content, default_content=content)
            s.add(tpl)
            await s.commit()
            await s.refresh(tpl)
        else:
            # versioning
            ver = MessageVersion(template_id=tpl.id, content=tpl.content, updated_by=updated_by)
            s.add(ver)
            tpl.content = content
            tpl.updated_at = datetime.datetime.utcnow()
            await s.commit()
            await s.refresh(tpl)
        return tpl

async def preview_template(content: str, sample_vars: Dict[str, str]) -> str:
    # Simple variable replacement
    result = content
    for k, v in sample_vars.items():
        result = result.replace(f"{{{{{k}}}}}", v)
    return result

async def get_setting(key: str):
    async with AsyncSessionLocal() as s:
        q = await s.execute(select(BotSetting).where(BotSetting.key == key))
        return q.scalars().first()

async def set_setting(key: str, value: Any):
    async with AsyncSessionLocal() as s:
        st = await get_setting(key)
        if not st:
            st = BotSetting(key=key, value=value)
            s.add(st)
            await s.commit()
            await s.refresh(st)
        else:
            st.value = value
            st.updated_at = datetime.datetime.utcnow()
            await s.commit()
            await s.refresh(st)
        return st
