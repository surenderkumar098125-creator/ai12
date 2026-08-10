from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey, Boolean, Text, JSON, func
from sqlalchemy.orm import relationship
from datetime import datetime
from .models import Base

def now():
    return datetime.utcnow()

class BotSetting(Base):
    __tablename__ = "bot_settings"
    id = Column(Integer, primary_key=True)
    key = Column(String(128), unique=True, index=True, nullable=False)
    value = Column(JSON, default={})
    updated_at = Column(DateTime, default=now)

class MessageTemplate(Base):
    __tablename__ = "message_templates"
    id = Column(Integer, primary_key=True)
    key = Column(String(128), unique=True, index=True, nullable=False)
    content = Column(Text, nullable=True)
    default_content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now)
    versions = relationship("MessageVersion", back_populates="template")

class MessageVersion(Base):
    __tablename__ = "message_versions"
    id = Column(Integer, primary_key=True)
    template_id = Column(ForeignKey("message_templates.id", ondelete="CASCADE"), index=True)
    content = Column(Text, nullable=True)
    updated_by = Column(BigInteger)
    created_at = Column(DateTime, default=now)
    template = relationship("MessageTemplate", back_populates="versions")

class WelcomeSetting(Base):
    __tablename__ = "welcome_settings"
    id = Column(Integer, primary_key=True)
    group_id = Column(BigInteger, index=True, nullable=False)
    enabled = Column(Boolean, default=True)
    message_template_id = Column(ForeignKey("message_templates.id", ondelete="SET NULL"), nullable=True)
    image_file_id = Column(String(512), nullable=True)
    buttons = Column(JSON, default=[])
    delete_after = Column(Integer, default=0)  # seconds, 0 means never
    updated_at = Column(DateTime, default=now)

class GoodbyeSetting(Base):
    __tablename__ = "goodbye_settings"
    id = Column(Integer, primary_key=True)
    group_id = Column(BigInteger, index=True, nullable=False)
    enabled = Column(Boolean, default=False)
    message_template_id = Column(ForeignKey("message_templates.id", ondelete="SET NULL"), nullable=True)
    image_file_id = Column(String(512), nullable=True)
    buttons = Column(JSON, default=[])
    updated_at = Column(DateTime, default=now)

class ButtonConfig(Base):
    __tablename__ = "button_configs"
    id = Column(Integer, primary_key=True)
    key = Column(String(128), index=True)
    text = Column(String(255))
    type = Column(String(32), default="url")  # url or callback
    payload = Column(String(1024))
    position = Column(Integer, default=0)
    created_at = Column(DateTime, default=now)

class Broadcast(Base):
    __tablename__ = "broadcasts"
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    content = Column(Text)
    media = Column(JSON, default=None)
    audience = Column(String(64), default="all_users")
    scheduled_at = Column(DateTime, nullable=True)
    created_by = Column(BigInteger)
    created_at = Column(DateTime, default=now)
    status = Column(String(32), default="pending")

class ScheduledBroadcast(Base):
    __tablename__ = "scheduled_broadcasts"
    id = Column(Integer, primary_key=True)
    broadcast_id = Column(ForeignKey("broadcasts.id", ondelete="CASCADE"), index=True)
    run_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=now)
    status = Column(String(32), default="scheduled")

class BroadcastLog(Base):
    __tablename__ = "broadcast_logs"
    id = Column(Integer, primary_key=True)
    broadcast_id = Column(ForeignKey("broadcasts.id", ondelete="CASCADE"), index=True)
    target_type = Column(String(32))
    target_id = Column(BigInteger)
    status = Column(String(32))
    error = Column(Text, nullable=True)
    sent_at = Column(DateTime, default=now)

# Lightweight AIRequest table used by Part 2 for rate limiting and analytics
class AIRequest(Base):
    __tablename__ = "ai_requests"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True)
    conversation_id = Column(String(255), index=True)
    prompt_hash = Column(String(128), nullable=True)
    model = Column(String(128), nullable=True)
    tokens_used = Column(Integer, default=0)
    status = Column(String(32), default="pending")
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=now)
