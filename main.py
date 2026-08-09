"""
Main CLI entrypoint for maintenance tasks.
This file intentionally does not start the bot yet — that will be added once handlers are in place.
"""
import argparse
import asyncio
from config import settings
from database import migrations, recovery

async def run_migrate():
    await migrations.upgrade()

async def run_backup():
    await recovery.create_backup()

async def run_restore(file: str):
    await recovery.restore_backup(file)

def main():
    parser = argparse.ArgumentParser("preeti_ultimate")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("migrate", help="Run database migrations (development create_all).")
    sub.add_parser("backup", help="Create database backup.")
    restore = sub.add_parser("restore", help="Restore database from backup.")
    restore.add_argument("--file", required=True)

    args = parser.parse_args()

    if args.cmd == "migrate":
        asyncio.run(run_migrate())
    elif args.cmd == "backup":
        asyncio.run(run_backup())
    elif args.cmd == "restore":
        asyncio.run(run_restore(args.file))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
