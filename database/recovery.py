from __future__ import annotations
import asyncio
import os
from pathlib import Path
import shutil
from datetime import datetime
from config import settings
from database import database
import aiofiles
import hashlib

BACKUP_DIR = Path(settings.BACKUP_DIR)
DB_URL = settings.DATABASE_URL

# This implementation currently supports SQLite file backups.
# For Postgres, extend with pg_dump/pg_restore or logical dumps.
def _sqlite_db_path_from_url(url: str) -> Path | None:
    # Expect sqlite+aiosqlite:///./data/dbname.db
    if url.startswith("sqlite"):
        # strip scheme and possible query
        # Example: sqlite+aiosqlite:///./data/db.db
        path = url.split("///", 1)[-1]
        return Path(path)
    return None

async def create_backup() -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    db_path = _sqlite_db_path_from_url(DB_URL)
    if db_path is None or not db_path.exists():
        raise RuntimeError("Backup currently supports a local SQLite database file; file not found.")
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    target = BACKUP_DIR / f"preeti_ultimate_{timestamp}.db"
    # Ensure the DB is consistent — perform a quick checkpoint before copying
    try:
        # For safety, run a checkpoint (works for sqlite)
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        conn.execute("PRAGMA wal_checkpoint(FULL);")
        conn.close()
    except Exception:
        pass
    shutil.copy2(db_path, target)
    # Save a quick checksum
    checksum = _file_checksum(target)
    meta = {"checksum": checksum, "created_at": timestamp}
    print(f"Created backup: {target} (checksum: {checksum})")
    return target

def _file_checksum(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

async def restore_backup(path_or_file: str):
    db_path = _sqlite_db_path_from_url(DB_URL)
    if db_path is None:
        raise RuntimeError("Restore currently supports only local SQLite database URL.")
    source = Path(path_or_file)
    if not source.exists():
        raise FileNotFoundError(f"Backup file not found: {source}")
    # Steps:
    # 1. Lock writes: here we only warn; in production, ensure the bot is stopped or use process-level lock
    print("Starting restore. Ensure the bot is stopped (writes locked).")
    # 2. Emergency backup
    emergency = await create_backup()
    print(f"Emergency backup created: {emergency}")
    # 3. Validate source (basic checksum / file exists)
    print(f"Validating backup {source}")
    checksum = _file_checksum(source)
    print(f"Backup checksum: {checksum}")
    # 4. Restore: copy file into place but do not delete anything else
    tmp_target = db_path.with_suffix(".restore_tmp")
    shutil.copy2(source, tmp_target)
    # 5. Replace live DB atomically
    backup_old = db_path.with_suffix(".pre_restore_backup")
    if db_path.exists():
        db_path.rename(backup_old)
    tmp_target.rename(db_path)
    print(f"Restored backup to {db_path}. Old DB saved at {backup_old}")
    # 6. Verify database health
    healthy = await database.check_database()
    if not healthy:
        print("Database verification failed after restore. Attempting to revert.")
        if backup_old.exists():
            backup_old.rename(db_path)
        raise RuntimeError("Restore failed verification; reverted to previous database.")
    print("Restore completed and verified. Remember to run migrations if needed.")
