from aiogram.fsm.middleware import BaseMiddleware

from modules.consumer.repository import ConsumerRepository


class ConsumerMiddleware(BaseMiddleware):
    def __init__(self, repository: ConsumerRepository) -> None:
        self.repository = repository

    async def __call__(self, handler, event, data):
        data["consumer"] = self.repository
        return await handler(event, data)
