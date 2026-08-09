"""Tic Tac Toe - simple turn-based game for two players"""
from ..base import BaseGame
from typing import Dict, Any, List

class TicTacToe(BaseGame):
    @classmethod
    def get_id(cls) -> str:
        return "tictactoe"

    @classmethod
    def get_name(cls) -> str:
        return "Tic Tac Toe"

    @classmethod
    def get_category(cls) -> str:
        return "classic"

    @classmethod
    def get_description(cls) -> str:
        return "Classic 3x3 Tic Tac Toe"

    async def start(self, **kwargs) -> Dict[str, Any]:
        # state: board as list of 9, current player (x/o), players mapping
        players = kwargs.get("players", [])
        state = {"board": [None]*9, "current": "X", "players": players}
        return {"state": state, "message": "TicTacToe started"}

    async def handle_input(self, session_state: Dict[str, Any], user_input: Any) -> Dict[str, Any]:
        # user_input expected: {"position":int, "symbol":"X"}
        pos = user_input.get("position")
        symbol = session_state["current"]
        board = session_state.get("board")
        if pos is None or pos < 0 or pos >= 9 or board[pos] is not None:
            return {"state": session_state, "message": "Invalid move"}
        board[pos] = symbol
        # check win
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b,c in wins:
            if board[a] and board[a]==board[b]==board[c]:
                session_state["score"] = 100 if symbol=="X" else 100
                return {"state": session_state, "finished": True, "message": f"{symbol} wins"}
        if all(board):
            session_state["score"] = 10
            return {"state": session_state, "finished": True, "message": "Draw"}
        session_state["current"] = "O" if symbol=="X" else "X"
        return {"state": session_state, "message": "Move accepted"}

    async def finish(self, session_state: Dict[str, Any]) -> Dict[str, Any]:
        return {"score": session_state.get("score",0)}

    def supports_multiplayer(self) -> bool:
        return True

    def calculate_score(self, session_state: Dict[str, Any]) -> int:
        return int(session_state.get("score",0))

    def calculate_reward(self, score: int, difficulty: str) -> Dict[str,int]:
        coins = score // 10
        return {"coins": coins, "xp": coins//2, "gems": 0}
