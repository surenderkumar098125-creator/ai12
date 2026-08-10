"""Registry for games"""
from typing import Dict, Type, List
from .base import BaseGame

class GameRegistry:
    def __init__(self):
        self._registry: Dict[str, Type[BaseGame]] = {}
        self._featured: List[str] = []

    def register(self, game_cls: Type[BaseGame]):
        gid = game_cls.get_id()
        self._registry[gid] = game_cls

    def get_game(self, gid: str) -> Type[BaseGame] | None:
        return self._registry.get(gid)

    def list_games(self) -> List[Type[BaseGame]]:
        return list(self._registry.values())

    def list_category(self, category: str):
        return [g for g in self._registry.values() if g.get_category() == category]

    def random_game(self):
        import random
        return random.choice(self.list_games()) if self._registry else None

    def search_games(self, query: str):
        q = query.lower()
        return [g for g in self._registry.values() if q in g.get_name().lower() or q in g.get_description().lower()]

    def set_featured(self, gid: str):
        if gid in self._registry and gid not in self._featured:
            self._featured.append(gid)

    def featured_games(self):
        return [self._registry[g] for g in self._featured if g in self._registry]

GAME_REGISTRY = GameRegistry()
