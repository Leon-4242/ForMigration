import logging

from aiogram import BaseMiddleware, Bot, Dispatcher, Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import Filter
from aiogram.types import BotCommand, BotCommandScope


class TelegramBot:
    def __init__(self, token):
        self.bot = Bot(token)
        self.dp = Dispatcher()
        self._polling = False

    def setup_outer_middlewares(self, middlewares: list[BaseMiddleware]):
        for middleware in middlewares:
            self.dp.update.outer_middleware(middleware)

    def setup_inner_middlewares(self, middlewares: list[BaseMiddleware]):
        for middleware in middlewares:
            self.dp.update.middleware(middleware)

    def setup_filters(self, filters: list[Filter]):
        for filter in filters:
            self.dp.update.filter(filter)

    def include_routers(self, routers: list[Router]):
        for router in routers:
            self.dp.include_router(router)

    async def setup_commands(
        self, commands: list[BotCommand], scope: BotCommandScope | None = None
    ):
        await self.bot.set_my_commands(commands, scope=scope)

    async def send_message(self, chat_id, *args, **kwargs):
        try:
            return await self.bot.send_message(chat_id, *args, **kwargs)
        except TelegramForbiddenError:
            logging.info(f"User {chat_id} blocked this bot")
        except Exception:
            logging.exception(f"Failed to send message to {chat_id}")
            raise

    async def send_photo(self, chat_id, *args, **kwargs):
        try:
            return await self.bot.send_photo(chat_id, *args, **kwargs)
        except TelegramForbiddenError:
            logging.info(f"User {chat_id} blocked this bot")
        except Exception:
            logging.exception(f"Failed to send photo to {chat_id}")
            raise

    async def start(self, startup_callback=None, *, skip_updates: bool = True):
        if startup_callback is not None:
            self.dp.startup.register(startup_callback)

        if skip_updates:
            await self.bot.delete_webhook(drop_pending_updates=True)

        self._polling = True
        try:
            await self.dp.start_polling(self.bot)
        finally:
            self._polling = False

    async def stop_polling(self) -> None:
        if self._polling:
            await self.dp.stop_polling()
            self._polling = False
