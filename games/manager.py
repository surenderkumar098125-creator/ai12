from __future__ import annotations
from .registry import GAME_REGISTRY
from .base import BaseGame
from typing import Dict, Any

class GameManager:
    def __init__(self):
        self.registry = GAME_REGISTRY

    def get_game(self, gid: str) -> BaseGame | None:
        cls = self.registry.get_game(gid)
        return cls() if cls else None

    def list_games(self):
        return self.registry.list_games()

    def start_game(self, gid: str, **kwargs) -> Dict[str, Any]:
        game = self.get_game(gid)
        if not game:
            raise ValueError("Game not found")
        # start returns initial payload; actual async start handled by async wrapper
        return {}
