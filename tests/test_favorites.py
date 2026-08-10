import pytest
from services.favorites import add_favorite, remove_favorite, list_favorites

import asyncio

@pytest.mark.asyncio
async def test_favorites_cycle():
    user = 123456789
    gid = 'rps'
    fav = await add_favorite(user, gid)
    assert fav.game_id == gid
    lst = await list_favorites(user)
    assert any(x.game_id==gid for x in lst)
    ok = await remove_favorite(user, gid)
    assert ok is True
