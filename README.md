# Preeti Ultimate — Part 1 (Core + Config + Database)

This commit bootstraps the Preeti Ultimate Telegram platform core pieces:

- Async configuration & environment validation (Pydantic).
- Async SQLAlchemy database layer configured for SQLite (WAL) and future Postgres migration.
- Database models for the main application schema (users, groups, economy, games, AI conversations, moderation, backup logs).
- Basic migration runner and safe backup/restore utilities.
- CLI skeleton for running migrations, backups and (later) the bot.

Next: Part 2 — AI integration (Groq), context manager, conversation memory, and AI handlers.

Environment
1. Copy `.env.example` to `.env` and fill secrets.
2. Create the data & backups folders:
   mkdir -p data backups logs

Install
pip install -r requirements.txt

Run migrations (development):
python main.py migrate

Make a backup:
python main.py backup

Restore (careful):
python main.py restore --file backups/preeti_ultimate_YYYYMMDD_HHMMSS.db

Notes
- No secrets or real tokens are committed.
- The database layer uses async SQLAlchemy and enforces PRAGMA foreign_keys=ON and WAL mode for SQLite.
- For production, replace sqlite URL with a Postgres URL and install psycopg[binary].
