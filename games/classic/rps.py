"""Rock Paper Scissors"""
from ..base import BaseGame
from typing import Dict, Any
import random

class RockPaperScissors(BaseGame):
    CHOICES = ["rock","paper","scissors"]

    @classmethod
    def get_id(cls) -> str:
        return "rps"

    @classmethod
    def get_name(cls) -> str:
        return "Rock Paper Scissors"

    @classmethod
    def get_category(cls) -> str:
        return "classic"

    async def start(self, **kwargs) -> Dict[str, Any]:
        state = {"bot_choice": random.choice(self.CHOICES)}
        return {"state": state, "message": "Choose rock/paper/scissors"}

    async def handle_input(self, session_state: Dict[str, Any], user_input: Any) -> Dict[str, Any]:
        u = (user_input or "").lower().strip()
        bot = session_state.get("bot_choice")
        if u not in self.CHOICES:
            return {"state": session_state, "message": "Invalid choice"}
        if u == bot:
            res = "draw"
            score = 10
        elif (u=="rock" and bot=="scissors") or (u=="paper" and bot=="rock") or (u=="scissors" and bot=="paper"):
            res = "win"
            score = 30
        else:
            res = "lose"
            score = 0
        session_state["score"] = score
        return {"state": session_state, "finished": True, "message": f"You {res}! Bot chose {bot}."}

    async def finish(self, session_state: Dict[str, Any]) -> Dict[str, Any]:
        return {"score": session_state.get("score",0)}

    def calculate_score(self, session_state: Dict[str, Any]) -> int:
        return int(session_state.get("score",0))

    def calculate_reward(self, score: int, difficulty: str) -> Dict[str,int]:
        coins = score // 10
        return {"coins": coins, "xp": coins//2, "gems": 0}
