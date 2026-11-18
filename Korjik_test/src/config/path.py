from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

SQLITE_DIR = DATA_DIR / "sqlite_db"
PICS_DIR = DATA_DIR / "pics"

USERS_DIR = SQLITE_DIR / "users.sqlite"
MESSAGES_DIR = SQLITE_DIR / "messages.sqlite"
