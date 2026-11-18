from typing import TYPE_CHECKING

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from infrastructure.scheduler.base_task import TaskGroup
from modules.base.task_ids import module_task_id

if TYPE_CHECKING:
    from modules.base.module import BotModule


class UpdateModuleTaskGroup(TaskGroup):
    """Стандартная TaskGroup модуля: периодический update()."""

    def __init__(
        self,
        module: "BotModule",
        scheduler: AsyncIOScheduler,
        *,
        interval_hours: int = 1,
    ) -> None:
        super().__init__(scheduler)
        self._module = module
        self._interval_hours = interval_hours

    @property
    def task_id(self) -> str:
        return module_task_id(self._module.id)

    async def start(self) -> None:
        self.scheduler.add_job(
            self._run_update,
            id=self.task_id,
            trigger="interval",
            hours=self._interval_hours,
        )

    async def shutdown(self) -> None:
        self.scheduler.remove_job(self.task_id)

    async def _run_update(self) -> None:
        self._module.update()
