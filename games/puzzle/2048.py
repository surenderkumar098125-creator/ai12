"""Simple 2048-like text game (compressed)"""
from ..base import BaseGame
from typing import Dict, Any
import random

class Game2048(BaseGame):
    @classmethod
    def get_id(cls) -> str:
        return "2048"

    @classmethod
    def get_name(cls) -> str:
        return "2048 (text)"

    @classmethod
    def get_category(cls) -> str:
        return "puzzle"

    async def start(self, **kwargs) -> Dict[str, Any]:
        # represent board as list of 16 ints
        board = [0]*16
        def add_tile(b):
            empties = [i for i,v in enumerate(b) if v==0]
            if not empties: return
            i = random.choice(empties)
            b[i] = 2 if random.random()<0.9 else 4
        add_tile(board); add_tile(board)
        state = {"board": board, "score": 0}
        return {"state": state, "message": "Use up/down/left/right to move."}

    async def handle_input(self, session_state: Dict[str, Any], user_input: Any) -> Dict[str, Any]:
        # simplified: random add and small scoring to simulate
        board = session_state.get("board")
        # perform a fake move
        import random
        session_state["score"] = session_state.get("score",0) + random.randint(0,10)
        return {"state": session_state, "message": "Moved", "finished": False}

    async def finish(self, session_state: Dict[str, Any]) -> Dict[str, Any]:
        return {"score": session_state.get("score",0)}

    def calculate_score(self, session_state: Dict[str, Any]) -> int:
        return int(session_state.get("score",0))

    def calculate_reward(self, score: int, difficulty: str) -> Dict[str,int]:
        coins = score // 20
        return {"coins": coins, "xp": coins//2, "gems": 0}
