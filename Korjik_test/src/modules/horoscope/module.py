from aiogram import Router
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from infrastructure.scheduler.base_task import TaskGroup
from modules.base import BotModule, ModuleId
from modules.base.repository import ModuleRepository
from modules.context import ModuleContext
from modules.horoscope.commands import HoroscopeBotCommands
from modules.horoscope.repository import HoroscopeRepository
from modules.horoscope.router import HoroscopeRouter
from modules.horoscope.service import HoroscopeService
from modules.horoscope.tasks import HoroscopeTaskGroup


class HoroscopeModule(BotModule):
    def __init__(self, context: ModuleContext) -> None:
        self._repository = HoroscopeRepository()
        self._service = HoroscopeService(
            repository=self._repository,
            messenger=context.messenger,
        )
        self._router = HoroscopeRouter(self._service)

    @property
    def id(self) -> ModuleId:
        return ModuleId.HOROSCOPE

    def get_router(self) -> Router:
        return self._router.get_router()

    @property
    def commands(self) -> list[BotCommand]:
        return list(HoroscopeBotCommands)

    def get_repository(self) -> ModuleRepository | None:
        return self._repository

    def build_tasks(
        self,
        scheduler: AsyncIOScheduler,
        *,
        interval_hours: int = 1,
    ) -> TaskGroup:
        task_group = HoroscopeTaskGroup(
            scheduler=scheduler,
            service=self._service,
            repository=self._repository,
        )
        self._service.bind_tasks(task_group)
        return task_group
