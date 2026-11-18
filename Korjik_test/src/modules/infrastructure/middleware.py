from aiogram.fsm.middleware import BaseMiddleware

from modules.infrastructure.repository import InfrastructureRepository


class InfrastructureMiddleware(BaseMiddleware):
    def __init__(self, repository: InfrastructureRepository) -> None:
        self.repository = repository

    async def __call__(self, handler, event, data):
        data["infrastructure"] = self.repository
        return await handler(event, data)
