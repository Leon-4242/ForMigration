from aiogram import Router
from aiogram.types import BotCommand

from modules.base import BotModule, ModuleId
from modules.base.repository import ModuleRepository
from modules.context import ModuleContext
from modules.infrastructure.commands import InfrastructureBotCommands
from modules.infrastructure.repository import InfrastructureRepository
from modules.infrastructure.router import InfrastructureRouter
from modules.infrastructure.service import InfrastructureService


class InfrastructureModule(BotModule):
    def __init__(self, context: ModuleContext) -> None:
        self._repository = InfrastructureRepository()
        self._service = InfrastructureService(
            repository=self._repository,
            source=context.google,
        )
        self._router = InfrastructureRouter(self._repository)

    @property
    def id(self) -> ModuleId:
        return ModuleId.INFRASTRUCTURE

    def get_router(self) -> Router:
        return self._router.get_router()

    @property
    def commands(self) -> list[BotCommand]:
        return list(InfrastructureBotCommands)

    def get_repository(self) -> ModuleRepository | None:
        return self._repository

    def update(self) -> None:
        self._service.update()
