from __future__ import annotations
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, JSON, Boolean, ForeignKey, UniqueConstraint
from .models import Base
from datetime import datetime

def now():
    return datetime.utcnow()

class FavoriteGame(Base):
    __tablename__ = "favorite_games"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True)
    game_id = Column(String(128), index=True)
    added_at = Column(DateTime, default=now)
    __table_args__ = (UniqueConstraint('user_id', 'game_id', name='uq_user_game_fav'),)

class RecentPlay(Base):
    __tablename__ = "recent_plays"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True)
    game_id = Column(String(128), index=True)
    last_played = Column(DateTime, default=now)
    best_score = Column(Integer, default=0)

class PlayerStats(Base):
    __tablename__ = "player_stats"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True, index=True)
    games_played = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    streak = Column(Integer, default=0)

class GameRoom(Base):
    __tablename__ = "game_rooms"
    id = Column(Integer, primary_key=True)
    room_id = Column(String(64), unique=True, index=True)
    game_id = Column(String(128), index=True)
    host_user_id = Column(BigInteger)
    max_players = Column(Integer, default=2)
    state = Column(String(32), default='WAITING')
    created_at = Column(DateTime, default=now)
    expires_at = Column(DateTime, nullable=True)
    metadata = Column(JSON, default={})

class Tournament(Base):
    __tablename__ = "tournaments"
    id = Column(Integer, primary_key=True)
    key = Column(String(128), unique=True, index=True)
    title = Column(String(255))
    game_id = Column(String(128), index=True)
    starts_at = Column(DateTime)
    ends_at = Column(DateTime)
    metadata = Column(JSON, default={})

class Quest(Base):
    __tablename__ = "quests"
    id = Column(Integer, primary_key=True)
    key = Column(String(128), unique=True, index=True)
    title = Column(String(255))
    description = Column(String(1024))
    criteria = Column(JSON, default={})
    reward = Column(JSON, default={})

class UserQuest(Base):
    __tablename__ = "user_quests"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True)
    quest_id = Column(ForeignKey('quests.id', ondelete='CASCADE'), index=True)
    progress = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)

class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True)
    key = Column(String(128), unique=True, index=True)
    title = Column(String(255))
    description = Column(String(1024))
    metadata = Column(JSON, default={})

class UserBadge(Base):
    __tablename__ = "user_badges"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True)
    badge_id = Column(ForeignKey('badges.id', ondelete='CASCADE'), index=True)
    awarded_at = Column(DateTime, default=now)

class DailyChallenge(Base):
    __tablename__ = "daily_challenge"
    id = Column(Integer, primary_key=True)
    date_key = Column(String(32), unique=True, index=True)
    game_id = Column(String(128), index=True)
    created_at = Column(DateTime, default=now)
    metadata = Column(JSON, default={})

class GameAnalytics(Base):
    __tablename__ = "game_analytics"
    id = Column(Integer, primary_key=True)
    game_id = Column(String(128), index=True)
    date = Column(DateTime, default=now)
    plays = Column(Integer, default=0)
    unique_players = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    total_score = Column(Integer, default=0)
    highest_score = Column(Integer, default=0)
    completions = Column(Integer, default=0)
