import pytest
from games.registry import GAME_REGISTRY
from games.base import BaseGame

def test_registry_register_and_lookup():
    # ensure registry has at least one registered game
    games = GAME_REGISTRY.list_games()
    assert len(games) > 0

