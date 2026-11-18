import os

from dotenv import load_dotenv

from config.path import BASE_DIR

load_dotenv(BASE_DIR / ".env")


def get_env(name: str, default: str | None = None, *, required: bool = False) -> str | None:
    value = os.getenv(name, default)
    if required and not value:
        raise RuntimeError(f"Переменная окружения {name!r} не задана")
    return value


BOT_TOKEN = get_env("BOT_TOKEN", required=True)
