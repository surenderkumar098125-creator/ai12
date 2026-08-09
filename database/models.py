from __future__ import annotations
from sqlalchemy import (
    Column, Integer, BigInteger, String, DateTime, ForeignKey, Boolean,
    Numeric, Text, JSON, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

def now():
    return datetime.utcnow()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String(255), nullable=True, index=True)
    display_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=now, nullable=False)
    # profile & settings stored as JSON for flexibility
    profile = Column(JSON, default={})
    settings = Column(JSON, default={})

    wallets = relationship("Wallet", back_populates="user", cascade="all, delete-orphan")
    vip = relationship("UserVIP", back_populates="user")

Index("ix_users_telegram_username", User.telegram_id, User.username)

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    group_id = Column(BigInteger, unique=True, index=True, nullable=False)  # telegram group id
    title = Column(String(512))
    owner_id = Column(BigInteger, nullable=True)
    settings = Column(JSON, default={})
    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime)

class GroupMember(Base):
    __tablename__ = "group_members"
    id = Column(Integer, primary_key=True)
    group_id = Column(ForeignKey("groups.id", ondelete="CASCADE"), index=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    joined_at = Column(DateTime, default=now)
    is_admin = Column(Boolean, default=False)

class GroupSetting(Base):
    __tablename__ = "group_settings"
    id = Column(Integer, primary_key=True)
    group_id = Column(ForeignKey("groups.id", ondelete="CASCADE"), unique=True)
    settings = Column(JSON, default={})
    updated_at = Column(DateTime, default=now)

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    coins = Column(Integer, default=0)
    gems = Column(Integer, default=0)
    xp = Column(Integer, default=0)
    updated_at = Column(DateTime, default=now)

    user = relationship("User", back_populates="wallets")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="SET NULL"), index=True, nullable=True)
    amount = Column(Integer, nullable=False)
    currency = Column(String(32), nullable=False)  # coins/gems/xp
    reason = Column(String(255), nullable=True)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=now)

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    key = Column(String(128), unique=True, index=True)
    name = Column(String(255))
    category = Column(String(64))
    meta = Column(JSON, default={})

class GameSession(Base):
    __tablename__ = "game_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    game_id = Column(ForeignKey("games.id", ondelete="SET NULL"), index=True)
    score = Column(Integer, default=0)
    started_at = Column(DateTime, default=now)
    finished_at = Column(DateTime, nullable=True)
    metadata = Column(JSON, default={})

class GameScore(Base):
    __tablename__ = "game_scores"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    game_id = Column(ForeignKey("games.id", ondelete="CASCADE"), index=True)
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=now)
    __table_args__ = (Index("ix_game_scores_user_game_score", "user_id", "game_id", "score"),)

class DailyReward(Base):
    __tablename__ = "daily_rewards"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    day = Column(Integer, nullable=False)
    claimed_at = Column(DateTime, default=now)

class Mission(Base):
    __tablename__ = "missions"
    id = Column(Integer, primary_key=True)
    key = Column(String(128), unique=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    reward = Column(JSON, default={})
    period = Column(String(32), default="daily")  # daily/weekly/monthly

class UserMission(Base):
    __tablename__ = "user_missions"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    mission_id = Column(ForeignKey("missions.id", ondelete="CASCADE"), index=True)
    progress = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=now)

class Achievement(Base):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True)
    key = Column(String(128), unique=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    reward = Column(JSON, default={})

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    achievement_id = Column(ForeignKey("achievements.id", ondelete="CASCADE"), index=True)
    unlocked_at = Column(DateTime, default=now)

class RedeemCode(Base):
    __tablename__ = "redeem_codes"
    id = Column(Integer, primary_key=True)
    code = Column(String(128), unique=True, index=True)
    payload = Column(JSON, default={})  # contains coins/gems/xp/vip_days
    max_uses = Column(Integer, default=1)
    uses = Column(Integer, default=0)
    per_user_limit = Column(Integer, default=1)
    expires_at = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True)

class Redemption(Base):
    __tablename__ = "redemptions"
    id = Column(Integer, primary_key=True)
    code_id = Column(ForeignKey("redeem_codes.id", ondelete="CASCADE"), index=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    created_at = Column(DateTime, default=now)
    metadata = Column(JSON, default={})

class VIPPlan(Base):
    __tablename__ = "vip_plans"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    days = Column(Integer)
    benefits = Column(JSON, default={})

class UserVIP(Base):
    __tablename__ = "user_vip"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    plan_id = Column(ForeignKey("vip_plans.id", ondelete="SET NULL"))
    started_at = Column(DateTime, default=now)
    expires_at = Column(DateTime, nullable=True)
    history = Column(JSON, default={})

class Friend(Base):
    __tablename__ = "friends"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    friend_id = Column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    created_at = Column(DateTime, default=now)
    UniqueConstraint("user_id", "friend_id", name="uq_friend_pair")

class Challenge(Base):
    __tablename__ = "challenges"
    id = Column(Integer, primary_key=True)
    challenger_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    challenged_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    game_id = Column(ForeignKey("games.id", ondelete="SET NULL"))
    expires_at = Column(DateTime)
    state = Column(String(32), default="pending")
    metadata = Column(JSON, default={})

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(String(255), index=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=now)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(ForeignKey("conversations.id", ondelete="CASCADE"), index=True)
    role = Column(String(32))  # user/assistant/system
    content = Column(Text)
    created_at = Column(DateTime, default=now)
    meta = Column(JSON, default={})

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    type = Column(String(128))
    actor_id = Column(ForeignKey("users.id", ondelete="SET NULL"))
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=now)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    type = Column(String(128))
    payload = Column(JSON, default={})
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=now)

class Warning(Base):
    __tablename__ = "warnings"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    group_id = Column(ForeignKey("groups.id", ondelete="CASCADE"))
    admin_id = Column(BigInteger)
    reason = Column(String(512))
    created_at = Column(DateTime, default=now)

class ModerationLog(Base):
    __tablename__ = "moderation_logs"
    id = Column(Integer, primary_key=True)
    action = Column(String(128))
    admin_id = Column(BigInteger)
    target_id = Column(BigInteger)
    group_id = Column(ForeignKey("groups.id", ondelete="SET NULL"))
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=now)

class Leaderboard(Base):
    __tablename__ = "leaderboards"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), index=True)
    payload = Column(JSON, default={})
    created_at = Column(DateTime, default=now)

class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True)
    key = Column(String(128), unique=True, index=True)
    value = Column(JSON, default={})

class AdminLog(Base):
    __tablename__ = "admin_logs"
    id = Column(Integer, primary_key=True)
    admin_id = Column(BigInteger)
    action = Column(String(255))
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=now)

# Shop items & purchases
class ShopItem(Base):
    __tablename__ = "shop_items"
    id = Column(Integer, primary_key=True)
    key = Column(String(128), unique=True, index=True)
    title = Column(String(255))
    price = Column(JSON, default={})
    meta = Column(JSON, default={})

class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="SET NULL"))
    item_id = Column(ForeignKey("shop_items.id", ondelete="SET NULL"))
    payload = Column(JSON, default={})
    created_at = Column(DateTime, default=now)

# Add any additional indexes or unique constraints below if required
