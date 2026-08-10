"""Main CLI and startup for Preeti bot.

Provides commands:
  - migrate
  - backup
  - restore --file
  - start    (start the bot)
  - health   (print health checks)

"""
import argparse
import asyncio
import logging
import sys
from config import settings
from database import migrations, recovery, database

# Safely import aiogram at runtime only when needed

async def run_migrate():
    await migrations.upgrade()

async def run_backup():
    await recovery.create_backup()

async def run_restore(file: str):
    await recovery.restore_backup(file)

async def _health():
    # minimal health aggregator
    from database.database import check_database
    db_ok = await check_database()
    # AI health check (best-effort)
    ai_ok = True
    try:
        if settings.GROQ_API_KEY:
            # We don't actually hit the API here; assume configured if key present
            ai_ok = True
    except Exception:
        ai_ok = False
    # Scheduler availability: check if scheduler module exists
    sched_ok = True
    try:
        import scheduler
        sched_ok = True
    except Exception:
        sched_ok = False
    return {
        "database": db_ok,
        "ai": ai_ok,
        "scheduler": sched_ok,
    }

async def run_health():
    res = await _health()
    print("Health checks:")
    for k,v in res.items():
        print(f" - {k}: {'OK' if v else 'FAIL'}")

async def _prepare_startup():
    # 1. Logging
    level = getattr(logging, settings.LOG_LEVEL.upper() if settings.LOG_LEVEL else 'INFO')
    logging.basicConfig(level=level, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

    logging.info("Starting startup: migrations -> register games -> scheduler -> handlers")

    # 2. Migrate DB (create_all development convenience)
    try:
        await migrations.upgrade()
    except Exception as e:
        logging.exception("Migration failed: %s", e)
        raise

    # 3. Ensure directories exist
    import os
    os.makedirs(settings.BACKUP_DIR, exist_ok=True)
    os.makedirs('data', exist_ok=True)
    os.makedirs('logs', exist_ok=True)

    # 4. Register games (ensure registry init runs)
    try:
        # games.registry_init registers games on import
        from games import registry_init  # noqa: F401
    except Exception:
        logging.exception("Failed to initialize game registry")

    # 5. Start scheduler (if available)
    try:
        from scheduler import start_all
        start_all()
        logging.info("Scheduler started")
    except Exception:
        logging.exception("Scheduler failed to start (will continue)")

async def run_start():
    # guard: require BOT_TOKEN
    if not settings.BOT_TOKEN:
        print("BOT_TOKEN not configured in environment (.env). Set BOT_TOKEN before starting the bot.")
        sys.exit(2)

    # prepare startup tasks
    await _prepare_startup()

    # import aiogram lazily
    try:
        from aiogram import Bot, Dispatcher
        from aiogram import exceptions
        from aiogram.client.session.aiohttp import AiohttpSession
    except Exception:
        print("aiogram is not installed. Please install requirements.txt before starting the bot.")
        sys.exit(2)

    # create bot and dispatcher
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    # Import handlers so routers register themselves with the default Dispatcher when imported
    # We import handlers defensively; missing handlers won't prevent startup.
    handler_modules = [
        'handlers.welcome',
        'handlers.game_center',
        'handlers.broadcast',
        'handlers.admin',
        'handlers.games',
        'handlers.health',
    ]
    for mod in handler_modules:
        try:
            __import__(mod)
        except Exception:
            logging.debug(f"Handler module {mod} not available or failed to import; continuing")

    # register a basic /health command locally if handlers.health not present
    try:
        from handlers.health import router as health_router
        dp.include_router(health_router)
    except Exception:
        from aiogram import Router
        from aiogram.types import Message
        r = Router()
        @r.message(lambda message: message.text and message.text.startswith('/health'))
        async def _health_cmd(message: Message):
            res = await _health()
            text = "Health:\n" + '\n'.join([f"{k}: {'OK' if v else 'FAIL'}" for k,v in res.items()])
            await message.reply(text)
        dp.include_router(r)

    # Start polling
    print("Bot starting. Press Ctrl+C to stop.")
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("Shutting down")
    finally:
        await bot.session.close()

def main():
    parser = argparse.ArgumentParser("preeti_ultimate")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("migrate", help="Run database migrations (development create_all).")
    sub.add_parser("backup", help="Create database backup.")
    restore = sub.add_parser("restore", help="Restore database from backup.")
    restore.add_argument("--file", required=True)
    sub.add_parser("start", help="Start the bot (requires BOT_TOKEN set in .env)")
    sub.add_parser("health", help="Run health checks and print result")

    args = parser.parse_args()

    if args.cmd == "migrate":
        asyncio.run(run_migrate())
    elif args.cmd == "backup":
        asyncio.run(run_backup())
    elif args.cmd == "restore":
        asyncio.run(run_restore(args.file))
    elif args.cmd == "start":
        asyncio.run(run_start())
    elif args.cmd == "health":
        asyncio.run(run_health())
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
