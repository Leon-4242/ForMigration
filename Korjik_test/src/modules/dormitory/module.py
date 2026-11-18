from aiogram import Router
from aiogram.types import BotCommand

from modules.base import BotModule, ModuleId
from modules.base.repository import ModuleRepository
from modules.context import ModuleContext
from modules.dormitory.commands import DormitoryBotCommands
from modules.dormitory.repository import DormitoryRepository
from modules.dormitory.router import DormitoryRouter
from modules.dormitory.service import DormitoryService


class DormitoryModule(BotModule):
    def __init__(self, context: ModuleContext) -> None:
        self._repository = DormitoryRepository()
        self._service = DormitoryService(
            repository=self._repository,
            source=context.google,
            messages=context.messages,
        )
        self._router = DormitoryRouter(self._repository)

    @property
    def id(self) -> ModuleId:
        return ModuleId.DORMITORY

    def get_router(self) -> Router:
        return self._router.get_router()

    @property
    def commands(self) -> list[BotCommand]:
        return list(DormitoryBotCommands)

    def get_repository(self) -> ModuleRepository | None:
        return self._repository

    def update(self) -> None:
        self._service.update()
