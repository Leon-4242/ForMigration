from pathlib import Path

from config.environment import get_env
from config.path import DATA_DIR

AUTH_DIR = Path(
    get_env(
        "GOOGLE_CREDENTIALS_FILE",
        str(DATA_DIR / "auth" / "korjik-tgbot.json"),
    )
)
SHEET_ID = get_env("SHEET_ID", required=True)
