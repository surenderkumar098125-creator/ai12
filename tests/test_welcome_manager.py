# tests/test_welcome_manager.py
import pytest
from services.welcome_manager import create_or_update_welcome, get_welcome_for_group, remove_welcome

@pytest.mark.asyncio
async def test_welcome_cycle():
    gid = -1001234567890
    ws = await create_or_update_welcome(gid, enabled=True, message_template_id=None, image_file_id=None, buttons=[], delete_after=0)
    assert ws.group_id == gid
    fetched = await get_welcome_for_group(gid)
    assert fetched is not None
    ok = await remove_welcome(gid)
    assert ok is True
