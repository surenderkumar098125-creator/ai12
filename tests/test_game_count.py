import pytest
from games.registry import GAME_REGISTRY

def test_game_count():
    games = GAME_REGISTRY.list_games()
    assert len(games) >= 75, f"Expected >=75 games, found {len(games)}"
