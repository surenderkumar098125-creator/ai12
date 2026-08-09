from __future__ import annotations
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, JSON, Text
from .models import Base
from datetime import datetime

def now():
    return datetime.utcnow()

class GameSession(Base):
    __tablename__ = "game_sessions"
    id = Column(Integer, primary_key=True)
    session_id = Column(String(64), unique=True, index=True, nullable=False)
    user_id = Column(BigInteger, index=True)
    group_id = Column(BigInteger, index=True, nullable=True)
    game_id = Column(String(128), index=True)
    difficulty = Column(String(32), default="normal")
    state = Column(JSON, default={})
    score = Column(Integer, default=0)
    started_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now)
    finished_at = Column(DateTime, nullable=True)
    status = Column(String(32), default="WAITING")

class GameScore(Base):
    __tablename__ = "game_scores"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True)
    game_id = Column(String(128), index=True)
    group_id = Column(BigInteger, index=True, nullable=True)
    score = Column(Integer, default=0)
    difficulty = Column(String(32), default="normal")
    duration = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=now)
