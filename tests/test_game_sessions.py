import pytest
from services.game_service import GameService

@pytest.mark.asyncio
async def test_start_game():
    svc = GameService()
    res = await svc.start_game_for_user('rps', 12345)
    assert 'session_id' in res
