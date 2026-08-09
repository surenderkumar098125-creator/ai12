from __future__ import annotations
from database.database import engine
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.game_events import GameEvents
from scheduler.game_scheduler import start_scheduler

scheduler = AsyncIOScheduler()

def start_all():
    start_scheduler()
    # add other startup tasks here
