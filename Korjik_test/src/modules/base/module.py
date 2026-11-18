from abc import ABC, abstractmethod

from aiogram import Router
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from infrastructure.scheduler.base_task import TaskGroup
from modules.base.repository import ModuleRepository
from modules.base.tasks import UpdateModuleTaskGroup
from modules.base.types import ModuleId


class BotModule(ABC):
    """
    Контракт feature-модуля для подключения к Application.

    У каждого модуля:
    - один внешний router (get_router);
    - один список BotCommand (commands) — только команды модуля, без system/admin;
    - одна группа фоновых задач (build_tasks → TaskGroup);
    - update/close для синхронизации и освобождения ресурсов.

    Подключение задач к infrastructure.scheduler.Scheduler:
        scheduler.add_module_tasks(modules)
        # или scheduler.add_task(UpdateModuleTaskGroup, module=module)
    """

    @property
    @abstractmethod
    def id(self) -> ModuleId:
        raise NotImplementedError

    @abstractmethod
    def get_router(self) -> Router:
        raise NotImplementedError

    @property
    def commands(self) -> list[BotCommand]:
        return []

    @abstractmethod
    def get_repository(self) -> ModuleRepository | None:
        """Репозиторий модуля или None, если модуль не использует локальное хранилище."""
        raise NotImplementedError

    def build_tasks(
        self,
        scheduler: AsyncIOScheduler,
        *,
        interval_hours: int = 1,
    ) -> TaskGroup:
        """По умолчанию — одна периодическая задача update()."""
        return UpdateModuleTaskGroup(self, scheduler, interval_hours=interval_hours)

    def update(self) -> None:
        """Синхронизация данных модуля (Sheets, cron-payload и т.д.)."""
        return None

    def close(self) -> None:
        repository = self.get_repository()
        if repository is not None:
            repository.close()
