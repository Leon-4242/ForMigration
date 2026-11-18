from aiogram import Router
from aiogram.types import BotCommand

from modules.base import BotModule, ModuleId
from modules.base.repository import ModuleRepository
from modules.consumer.commands import ConsumerBotCommands
from modules.consumer.repository import ConsumerRepository
from modules.consumer.router import ConsumerRouter
from modules.consumer.service import ConsumerService
from modules.context import ModuleContext


class ConsumerModule(BotModule):
    def __init__(self, context: ModuleContext) -> None:
        self._repository = ConsumerRepository()
        self._service = ConsumerService(
            repository=self._repository,
            source=context.google,
        )
        self._router = ConsumerRouter(self._repository)

    @property
    def id(self) -> ModuleId:
        return ModuleId.CONSUMER

    def get_router(self) -> Router:
        return self._router.get_router()

    @property
    def commands(self) -> list[BotCommand]:
        return list(ConsumerBotCommands)

    def get_repository(self) -> ModuleRepository | None:
        return self._repository

    def update(self) -> None:
        self._service.update()
