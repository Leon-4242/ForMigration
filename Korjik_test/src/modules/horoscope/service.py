from __future__ import annotations

import html
import logging
import random
from pathlib import Path
from typing import TYPE_CHECKING

import httpx
from aiogram.enums import ParseMode
from bs4 import BeautifulSoup

from infrastructure.services.messenger import MessengerService
from models.user import User
from modules.horoscope.config import HOROSCOPE_PICS_DIR
from modules.horoscope.repository import HoroscopeRepository
from modules.horoscope.types import HoroscopeSign, HoroscopeUser

if TYPE_CHECKING:
    from modules.horoscope.tasks import HoroscopeTaskGroup

_GREETINGS = [
    "🇺🇸🇺🇸 Good morning 🇺🇸🇺🇸",
    "🇷🇸🇷🇸 Добро јутро 🇷🇸🇷🇸",
    "🇫🇷🇫🇷 Bonjour 🇫🇷🇫🇷",
    "🇮🇹🇮🇹 Buongiorno 🇮🇹🇮🇹",
    "🇫🇮🇫🇮 Huomenta 🇫🇮🇫🇮",
    "🇸🇪🇸🇪 God morgon 🇸🇪🇸🇪",
    "🇩🇪🇩🇪 Guten Morgen 🇩🇪🇩🇪",
    "🇬🇷🇬🇷 Καλημέρα 🇬🇷🇬🇷",
]

_HOROSCOPE_URL = "https://horo.mail.ru/prediction/{sign}/today/"
_FALLBACK_HOROSCOPE = "К сожалению, сегодня не удалось получить гороскоп."


class HoroscopeService:
    DEFAULT_SIGN = HoroscopeSign.LEO
    DEFAULT_HOUR = 7
    DEFAULT_MINUTE = 0

    def __init__(
        self,
        repository: HoroscopeRepository,
        messenger: MessengerService,
        *,
        pics_dir: Path = HOROSCOPE_PICS_DIR,
    ) -> None:
        self.repository = repository
        self.messenger = messenger
        self.pics_dir = pics_dir
        self.client = httpx.AsyncClient()
        self.horoscopes: dict[str, str] = {}
        self._tasks: HoroscopeTaskGroup | None = None

    def bind_tasks(self, tasks: HoroscopeTaskGroup) -> None:
        self._tasks = tasks

    async def add_subscription(
        self,
        telegram_id: int,
        username: str | None,
        *,
        sign: HoroscopeSign | None = None,
        hour: int | None = None,
        minute: int | None = None,
    ) -> bool:
        if self.repository.is_subscribed(telegram_id):
            return False

        self.repository.add_sub(
            telegram_id=telegram_id,
            username=username or "",
            sign=sign or self.DEFAULT_SIGN,
            hour=hour if hour is not None else self.DEFAULT_HOUR,
            minute=minute if minute is not None else self.DEFAULT_MINUTE,
        )
        user = self.repository.get_user(telegram_id)
        if user is not None and self._tasks is not None:
            await self._tasks.schedule_user(user)
        return True

    async def remove_subscription(self, telegram_id: int) -> bool:
        user = self.repository.get_user(telegram_id)
        if user is None:
            return False

        if self._tasks is not None:
            await self._tasks.remove_user(user)
        self.repository.del_sub(telegram_id)
        return True

    async def set_notify_time(self, telegram_id: int, hour: int, minute: int) -> bool:
        if not self.repository.is_subscribed(telegram_id):
            return False

        self.repository.set_notify_time(telegram_id, hour, minute)
        user = self.repository.get_user(telegram_id)
        if user is not None and self._tasks is not None:
            await self._tasks.reschedule_user(user)
        return True

    async def load_horoscopes(self) -> None:
        for sign in HoroscopeSign:
            url = _HOROSCOPE_URL.format(sign=sign.value)
            try:
                response = await self.client.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")
                article = soup.find(
                    "div",
                    class_="article__item article__item_alignment_left article__item_html",
                )
                if article is None:
                    raise ValueError("Horoscope not found")

                horoscope = html.escape(article.get_text(strip=True))
            except (httpx.HTTPError, ValueError):
                logging.exception("Failed to load horoscope for %s", sign.value)
                horoscope = _FALLBACK_HOROSCOPE

            self.horoscopes[sign.value] = horoscope

    def build_message(self, user: HoroscopeUser) -> tuple[str, str | None]:
        horoscope = self.horoscopes.get(user.horoscope_sign.value, _FALLBACK_HOROSCOPE)
        text = (
            f"{random.choice(_GREETINGS)}\n"
            f"<b>Гороскоп на сегодня {user.horoscope_sign.symbol}</b>\n\n"
            f"<tg-spoiler>{horoscope}</tg-spoiler>\n\n"
            f"<i>{user.notify_time.strftime('%H:%M')}</i>"
        )
        photo = self._pick_photo()
        return text, photo

    async def notify_user(self, user: HoroscopeUser) -> None:
        text, photo = self.build_message(user)
        await self.messenger.send_message(
            user=User(telegram_id=user.telegram_id, name=user.telegram_name),
            text=text,
            photo=photo,
            parse_mode=ParseMode.HTML,
        )

    def _pick_photo(self) -> str | None:
        if not self.pics_dir.exists():
            return None

        images = [path for path in self.pics_dir.iterdir() if path.is_file()]
        if not images:
            return None

        return str(random.choice(images))

    async def close(self) -> None:
        await self.client.aclose()
