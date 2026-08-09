"""Reaction Test - simple action game"""
from ..base import BaseGame
from typing import Dict, Any
import time
import random

class ReactionTest(BaseGame):
    @classmethod
    def get_id(cls) -> str:
        return "reaction_test"

    @classmethod
    def get_name(cls) -> str:
        return "Reaction Test"

    @classmethod
    def get_category(cls) -> str:
        return "action"

    @classmethod
    def get_description(cls) -> str:
        return "Test your reaction time."

    async def start(self, **kwargs) -> Dict[str, Any]:
        # send a 'get ready' then start time
        wait = random.uniform(1.0, 3.0)
        state = {"started": False, "start_time": None, "wait": wait}
        return {"state": state, "message": f"Get ready... will start in {wait:.1f}s"}

    async def handle_input(self, session_state: Dict[str, Any], user_input: Any) -> Dict[str, Any]:
        # user_input is 'tap' when they tap; if tapped before start => false start
        state = session_state
        now = time.time()
        if not state.get("started"):
            # if wait elapsed, start
            state["started"] = True
            state["start_time"] = now
            return {"state": state, "message": "GO!"}
        else:
            # calculate reaction
            start = state.get("start_time") or now
            reaction = (now - start) * 1000
            state["score"] = int(max(0, 2000 - reaction))
            return {"state": state, "finished": True, "message": f"Reaction: {reaction:.0f}ms"}

    async def finish(self, session_state: Dict[str, Any]) -> Dict[str, Any]:
        score = session_state.get("score", 0)
        return {"score": score}

    def calculate_score(self, session_state: Dict[str, Any]) -> int:
        return int(session_state.get("score", 0))

    def calculate_reward(self, score: int, difficulty: str) -> Dict[str,int]:
        base = max(1, score // 50)
        return {"coins": base, "xp": base//2, "gems": 0}
