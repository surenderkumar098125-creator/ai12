from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.broadcast_manager import send_broadcast
from database.database import engine
import asyncio
import logging

logger = logging.getLogger("preeti.scheduler.broadcast")

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.start()

async def schedule_pending():
    # This would scan scheduled_broadcasts table and schedule jobs
    pass
