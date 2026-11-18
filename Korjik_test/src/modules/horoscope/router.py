from aiogram.filters import Command

from modules.base.router import ModuleRouter
from modules.horoscope import handlers
from modules.horoscope.commands import HoroscopeCommands
from modules.horoscope.middleware import HoroscopeMiddleware
from modules.horoscope.service import HoroscopeService


class HoroscopeRouter(ModuleRouter):
    def __init__(self, service: HoroscopeService) -> None:
        super().__init__()
        middleware = HoroscopeMiddleware(service)
        self.router.message.middleware(middleware)
        self.register_handlers()

    def register_handlers(self) -> None:
        router = self.router

        router.message.register(
            handlers.command_help,
            Command(HoroscopeCommands.HELP),
        )
        router.message.register(
            handlers.command_subscribe,
            Command(HoroscopeCommands.SUB),
        )
        router.message.register(
            handlers.command_unsubscribe,
            Command(HoroscopeCommands.UNSUB),
        )
        router.message.register(
            handlers.command_set_time,
            Command(HoroscopeCommands.TIME),
        )
