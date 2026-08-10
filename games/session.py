from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class GameSessionState:
    session_id: str
    user_id: int
    group_id: Optional[int]
    game_id: str
    difficulty: str
    state: dict
    score: int = 0
    started_at: datetime | None = None
    updated_at: datetime | None = None
    finished_at: datetime | None = None
    status: str = "WAITING"
