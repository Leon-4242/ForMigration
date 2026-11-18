from aiogram.fsm.middleware import BaseMiddleware

from modules.horoscope.service import HoroscopeService


class HoroscopeMiddleware(BaseMiddleware):
    def __init__(self, service: HoroscopeService) -> None:
        self.service = service

    async def __call__(self, handler, event, data):
        data["horoscope"] = self.service
        return await handler(event, data)
