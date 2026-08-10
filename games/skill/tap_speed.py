"""Tap Speed - count taps in time window"""
from ..base import BaseGame
from typing import Dict, Any
import time

class TapSpeed(BaseGame):
    @classmethod
    def get_id(cls) -> str:
        return "tap_speed"

    @classmethod
    def get_name(cls) -> str:
        return "Tap Speed"

    @classmethod
    def get_category(cls) -> str:
        return "skill"

    async def start(self, **kwargs) -> Dict[str, Any]:
        duration = kwargs.get("duration", 5)
        state = {"duration": duration, "start_time": time.time(), "taps": 0}
        return {"state": state, "message": f"Tap as fast as you can for {duration}s"}

    async def handle_input(self, session_state: Dict[str, Any], user_input: Any) -> Dict[str, Any]:
        state = session_state
        state["taps"] = state.get("taps", 0) + 1
        elapsed = time.time() - state.get("start_time")
        if elapsed >= state.get("duration"):
            state["score"] = state["taps"]
            return {"state": state, "finished": True, "message": f"Taps: {state['taps']}"}
        return {"state": state, "message": f"Taps: {state['taps']}"}

    async def finish(self, session_state: Dict[str, Any]) -> Dict[str, Any]:
        return {"score": session_state.get("score", 0)}

    def calculate_score(self, session_state: Dict[str, Any]) -> int:
        return int(session_state.get("score", 0))

    def calculate_reward(self, score: int, difficulty: str) -> Dict[str,int]:
        coins = max(1, score // 5)
        return {"coins": coins, "xp": coins//2, "gems": 0}
