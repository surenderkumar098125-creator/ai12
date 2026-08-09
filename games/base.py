from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseGame(ABC):
    """Abstract base for all games."""

    @classmethod
    @abstractmethod
    def get_id(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        pass

    @classmethod
    def get_category(cls) -> str:
        return "general"

    @classmethod
    def get_description(cls) -> str:
        return ""

    @classmethod
    def get_instructions(cls) -> str:
        return ""

    @abstractmethod
    async def start(self, **kwargs) -> Dict[str, Any]:
        """Start a game session. Return initial state/result payload."""
        pass

    @abstractmethod
    async def handle_input(self, session_state: Dict[str, Any], user_input: Any) -> Dict[str, Any]:
        """Handle user input and update session state. Return updated state and optional result."""
        pass

    @abstractmethod
    async def finish(self, session_state: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def calculate_score(self, session_state: Dict[str, Any]) -> int:
        pass

    @abstractmethod
    def calculate_reward(self, score: int, difficulty: str) -> Dict[str,int]:
        pass

    def supports_group(self) -> bool:
        return False

    def supports_multiplayer(self) -> bool:
        return False

    def supports_timer(self) -> bool:
        return False

    def supports_difficulty(self) -> bool:
        return False
