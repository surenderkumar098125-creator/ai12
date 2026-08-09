from __future__ import annotations
from typing import Optional
from database.database import AsyncSessionLocal
from database.content_models import WelcomeSetting
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import datetime

async def get_welcome_for_group(group_id: int) -> Optional[WelcomeSetting]:
    async with AsyncSessionLocal() as s:
        q = await s.execute(select(WelcomeSetting).where(WelcomeSetting.group_id == group_id))
        return q.scalars().first()

async def create_or_update_welcome(group_id: int, enabled: bool = True, message_template_id: int | None = None, image_file_id: str | None = None, buttons: list | None = None, delete_after: int = 0):
    async with AsyncSessionLocal() as s:
        ws = await get_welcome_for_group(group_id)
        if not ws:
            ws = WelcomeSetting(group_id=group_id, enabled=enabled, message_template_id=message_template_id, image_file_id=image_file_id, buttons=buttons or [], delete_after=delete_after)
            s.add(ws)
            await s.commit()
            await s.refresh(ws)
            return ws
        ws.enabled = enabled
        ws.message_template_id = message_template_id
        ws.image_file_id = image_file_id
        ws.buttons = buttons or []
        ws.delete_after = delete_after
        ws.updated_at = datetime.datetime.utcnow()
        await s.commit()
        await s.refresh(ws)
        return ws

async def remove_welcome(group_id: int):
    async with AsyncSessionLocal() as s:
        q = await s.execute(select(WelcomeSetting).where(WelcomeSetting.group_id == group_id))
        ws = q.scalars().first()
        if ws:
            await s.delete(ws)
            await s.commit()
            return True
        return False
