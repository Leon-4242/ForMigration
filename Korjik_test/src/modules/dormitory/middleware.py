from aiogram.fsm.middleware import BaseMiddleware

from modules.dormitory.repository import DormitoryRepository


class DormitoryMiddleware(BaseMiddleware):
    def __init__(self, repository: DormitoryRepository) -> None:
        self.repository = repository

    async def __call__(self, handler, event, data):
        data["dormitory"] = self.repository
        return await handler(event, data)
