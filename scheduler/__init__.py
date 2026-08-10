from apscheduler.schedulers.asyncio import AsyncIOScheduler
from scheduler.game_scheduler import start_scheduler as start_game_scheduler
from scripts.daily_challenge_selector import select_daily_challenge
import asyncio

scheduler = AsyncIOScheduler()

def start_all():
    # start existing game scheduler
    start_game_scheduler()
    # schedule daily challenge selection at 00:05 UTC daily
    scheduler.add_job(lambda: asyncio.create_task(select_daily_challenge()), 'cron', hour=0, minute=5)
    scheduler.start()
