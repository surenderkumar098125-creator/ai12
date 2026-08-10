import pytest
from games.registry import GAME_REGISTRY

def test_game_center_entries():
    games = GAME_REGISTRY.list_games()
    assert len(games) >= 75

