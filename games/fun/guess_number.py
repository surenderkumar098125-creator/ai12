"""Guess Number game"""
from ..base import BaseGame
from typing import Dict, Any
import random

class GuessNumber(BaseGame):
    @classmethod
    def get_id(cls) -> str:
        return "guess_number"

    @classmethod
    def get_name(cls) -> str:
        return "Guess Number"

    @classmethod
    def get_category(cls) -> str:
        return "fun"

    async def start(self, **kwargs) -> Dict[str, Any]:
        low = kwargs.get("low",1)
        high = kwargs.get("high",100)
        target = random.randint(low, high)
        state = {"target": target, "attempts": 0}
        return {"state": state, "message": f"I'm thinking of a number between {low} and {high}. Guess!"}

    async def handle_input(self, session_state: Dict[str, Any], user_input: Any) -> Dict[str, Any]:
        try:
            guess = int(user_input)
        except Exception:
            return {"state": session_state, "message": "Please send a number."}
        session_state["attempts"] = session_state.get("attempts",0) + 1
        target = session_state.get("target")
        if guess == target:
            session_state["score"] = max(0, 100 - (session_state["attempts"]-1)*10)
            return {"state": session_state, "finished": True, "message": f"Correct! Attempts: {session_state['attempts']}"}
        elif guess < target:
            return {"state": session_state, "message": "Higher"}
        else:
            return {"state": session_state, "message": "Lower"}

    async def finish(self, session_state: Dict[str, Any]) -> Dict[str, Any]:
        return {"score": session_state.get("score",0)}

    def calculate_score(self, session_state: Dict[str, Any]) -> int:
        return int(session_state.get("score",0))

    def calculate_reward(self, score: int, difficulty: str) -> Dict[str,int]:
        coins = score // 10
        return {"coins": coins, "xp": coins//2, "gems": 0}
